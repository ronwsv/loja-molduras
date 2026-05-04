import { env } from '$env/dynamic/private';

export async function load({ fetch }) {
  const base = env.PRIVATE_API_BASE || 'http://localhost:8000/api';
  try {
    const [featuredProducts, categories] = await Promise.all([
      fetch(`${base}/products/featured`).then((r: Response) => (r.ok ? r.json() : [])),
      fetch(`${base}/categories`).then((r: Response) => (r.ok ? r.json() : [])),
    ]);
    return { featuredProducts, categories };
  } catch {
    return { featuredProducts: [], categories: [] };
  }
}
