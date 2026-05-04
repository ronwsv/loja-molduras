import { env } from '$env/dynamic/private';

export async function load({ fetch, url }) {
  const base = env.PRIVATE_API_BASE || 'http://localhost:8000/api';
  const params = new URLSearchParams();
  const categoryId = url.searchParams.get('category_id');
  const search = url.searchParams.get('search');
  if (categoryId) params.set('category_id', categoryId);
  if (search) params.set('search', search);
  const qs = params.toString();

  try {
    const [products, categories] = await Promise.all([
      fetch(`${base}/products${qs ? `?${qs}` : ''}`).then((r: Response) => (r.ok ? r.json() : [])),
      fetch(`${base}/categories`).then((r: Response) => (r.ok ? r.json() : [])),
    ]);
    return { products, categories };
  } catch {
    return { products: [], categories: [] };
  }
}
