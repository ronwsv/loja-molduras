<script lang="ts">
  import { onMount } from 'svelte';
  import { api } from '$lib/api';

  let products: any[] = $state([]);
  let categories: any[] = $state([]);
  let loading = $state(true);

  onMount(async () => {
    try {
      [products, categories] = await Promise.all([
        api.adminGetProducts(),
        api.adminGetCategories(),
      ]);
    } catch { /* handled by layout auth */ }
    loading = false;
  });

  let featured = $derived(products.filter((p: any) => p.featured).length);
</script>

<svelte:head><title>Dashboard - Admin</title></svelte:head>

<div class="page-header">
  <h1>Dashboard</h1>
  <p>Bem-vindo ao painel de administração</p>
</div>

{#if loading}
  <p class="loading">Carregando...</p>
{:else}
  <div class="stats-grid">
    <div class="stat-card">
      <div class="stat-icon blue">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 01-8 0"/></svg>
      </div>
      <div>
        <div class="stat-value">{products.length}</div>
        <div class="stat-label">Total de Produtos</div>
      </div>
    </div>
    <div class="stat-card">
      <div class="stat-icon yellow">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
      </div>
      <div>
        <div class="stat-value">{featured}</div>
        <div class="stat-label">Em Destaque</div>
      </div>
    </div>
    <div class="stat-card">
      <div class="stat-icon green">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 19a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h5l2 3h9a2 2 0 012 2z"/></svg>
      </div>
      <div>
        <div class="stat-value">{categories.length}</div>
        <div class="stat-label">Categorias</div>
      </div>
    </div>
  </div>

  <div class="quick-links">
    <h2>Ações rápidas</h2>
    <div class="links-row">
      <a href="/admin/produtos" class="quick-link">Gerenciar Produtos</a>
      <a href="/admin/categorias" class="quick-link">Gerenciar Categorias</a>
      <a href="/admin/banners" class="quick-link">Gerenciar Banners</a>
    </div>
  </div>
{/if}

<style>
  .page-header { margin-bottom: 2rem; }
  .page-header h1 { font-size: 1.6rem; margin: 0 0 0.25rem; color: #1a1a2e; }
  .page-header p { color: #666; margin: 0; }

  .loading { color: #888; }

  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1rem;
    margin-bottom: 2.5rem;
  }

  .stat-card {
    background: #fff;
    border-radius: 10px;
    padding: 1.25rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  }

  .stat-icon {
    width: 48px; height: 48px;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
  }

  .stat-icon.blue { background: #e8f4ff; color: #2d6cdf; }
  .stat-icon.yellow { background: #fff8e1; color: #f5b800; }
  .stat-icon.green { background: #e8f8ee; color: #27ae60; }

  .stat-value { font-size: 1.8rem; font-weight: 700; color: #1a1a2e; line-height: 1; }
  .stat-label { font-size: 0.8rem; color: #888; margin-top: 4px; }

  .quick-links h2 { font-size: 1rem; color: #444; margin: 0 0 0.75rem; }
  .links-row { display: flex; gap: 0.75rem; flex-wrap: wrap; }

  .quick-link {
    padding: 0.6rem 1.25rem;
    background: #1a1a2e;
    color: #f5b800;
    border-radius: 8px;
    text-decoration: none;
    font-size: 0.9rem;
    font-weight: 600;
    transition: opacity 0.15s;
  }
  .quick-link:hover { opacity: 0.85; }
</style>
