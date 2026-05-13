import { env } from '$env/dynamic/public';
const API_BASE = env.PUBLIC_API_BASE || 'http://localhost:8000/api';

async function request(endpoint: string, options: RequestInit = {}) {
  const token = typeof localStorage !== 'undefined' ? localStorage.getItem('token') : null;
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...((options.headers as Record<string, string>) || {}),
  };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers,
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: 'Erro de conexão' }));
    throw new Error(error.detail || `Erro ${res.status}`);
  }

  if (res.status === 204) return null;
  return res.json();
}

export const api = {
  // Auth (admin only)
  login: (data: { email: string; password: string }) =>
    request('/auth/login', { method: 'POST', body: JSON.stringify(data) }),

  getMe: () => request('/auth/me'),

  changePassword: (data: { current_password: string; new_password: string }) =>
    request('/auth/me/password', { method: 'PUT', body: JSON.stringify(data) }),

  // Products
  getProducts: (params?: { category_id?: number; search?: string }) => {
    const query = new URLSearchParams();
    if (params?.category_id) query.set('category_id', String(params.category_id));
    if (params?.search) query.set('search', params.search);
    const qs = query.toString();
    return request(`/products${qs ? `?${qs}` : ''}`);
  },

  getFeaturedProducts: () => request('/products/featured'),

  getProduct: (id: number) => request(`/products/${id}`),

  // Banners
  getBanners: () => request('/banners'),
  adminGetBanners: () => request('/admin/banners'),
  adminCreateBanner: (data: object) => request('/admin/banners', { method: 'POST', body: JSON.stringify(data) }),
  adminUpdateBanner: (id: number, data: object) => request(`/admin/banners/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  adminDeleteBanner: (id: number) => request(`/admin/banners/${id}`, { method: 'DELETE' }),

  // Categories
  getCategories: () => request('/categories'),

  // Admin: Categories
  adminGetCategories: () => request('/admin/categories'),
  adminCreateCategory: (data: { name: string; image_url: string }) =>
    request('/admin/categories', { method: 'POST', body: JSON.stringify(data) }),
  adminUpdateCategory: (id: number, data: { name: string; image_url: string }) =>
    request(`/admin/categories/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  adminDeleteCategory: (id: number) =>
    request(`/admin/categories/${id}`, { method: 'DELETE' }),

  // Admin: Products
  adminGetProducts: () => request('/admin/products'),
  adminCreateProduct: (data: {
    name: string; description: string;
    images: string[]; category_id: number; featured: boolean;
  }) => request('/admin/products', { method: 'POST', body: JSON.stringify(data) }),
  adminUpdateProduct: (id: number, data: {
    name: string; description: string;
    images: string[]; category_id: number; featured: boolean;
  }) => request(`/admin/products/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  adminDeleteProduct: (id: number) =>
    request(`/admin/products/${id}`, { method: 'DELETE' }),

  // Admin: Upload
  uploadImage: async (file: File): Promise<{ url: string }> => {
    const token = typeof localStorage !== 'undefined' ? localStorage.getItem('token') : null;
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch(`${API_BASE}/admin/upload`, {
      method: 'POST',
      headers: token ? { Authorization: `Bearer ${token}` } : {},
      body: formData,
    });
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Erro no upload' }));
      throw new Error(error.detail || `Erro ${res.status}`);
    }
    return res.json();
  },
};
