<script lang="ts">
  import { goto } from '$app/navigation';
  import { page } from '$app/state';
  import ProductGrid from '$lib/components/ProductGrid.svelte';

  let { data } = $props();

  let searchQuery = $state(page.url.searchParams.get('search') || '');
  let selectedCategory = $state(
    page.url.searchParams.get('category_id') ? Number(page.url.searchParams.get('category_id')) : null
  );

  function applyFilters() {
    const params = new URLSearchParams();
    if (selectedCategory) params.set('category_id', String(selectedCategory));
    if (searchQuery.trim()) params.set('search', searchQuery.trim());
    goto(`/produtos${params.toString() ? `?${params}` : ''}`, { replaceState: false, invalidateAll: true });
  }

  function selectCategory(id: number | null) {
    selectedCategory = id;
    const params = new URLSearchParams();
    if (id) params.set('category_id', String(id));
    if (searchQuery.trim()) params.set('search', searchQuery.trim());
    goto(`/produtos${params.toString() ? `?${params}` : ''}`, { replaceState: false, invalidateAll: true });
  }

  function handleSearch(e: Event) {
    e.preventDefault();
    applyFilters();
  }
</script>

<svelte:head>
  <title>Produtos - Molduras Novo Tempo</title>
</svelte:head>

<section class="catalog">
  <div class="container">
    <h1 class="section-title">Nossos Produtos</h1>

    <div class="filters">
      <div class="category-filters">
        <button
          class="filter-btn"
          class:active={!selectedCategory}
          onclick={() => selectCategory(null)}
        >Todos</button>
        {#each data.categories as cat}
          <button
            class="filter-btn"
            class:active={selectedCategory === cat.id}
            onclick={() => selectCategory(cat.id)}
          >{cat.name}</button>
        {/each}
      </div>

      <form class="search-form" onsubmit={handleSearch}>
        <input
          type="text"
          placeholder="Buscar produtos..."
          bind:value={searchQuery}
        />
        <button type="submit" class="btn btn-primary">Buscar</button>
      </form>
    </div>

    {#if data.products.length === 0}
      <div class="empty">
        <p>Nenhum produto encontrado.</p>
        <a href="/produtos" class="btn btn-outline">Ver todos os produtos</a>
      </div>
    {:else}
      <p class="results-count">{data.products.length} produto{data.products.length !== 1 ? 's' : ''} encontrado{data.products.length !== 1 ? 's' : ''}</p>
      <ProductGrid products={data.products} />
    {/if}
  </div>
</section>

<style>
  .catalog {
    padding: 2rem 0 4rem;
  }

  .filters {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
    margin-bottom: 2rem;
  }

  .category-filters {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .filter-btn {
    padding: 0.5rem 1rem;
    border: 2px solid var(--gray-200);
    border-radius: 50px;
    font-size: 0.85rem;
    font-weight: 500;
    color: var(--gray-600);
    transition: all 0.2s;
    background: var(--white);
  }

  .filter-btn:hover {
    border-color: var(--primary);
    color: var(--primary-dark);
  }

  .filter-btn.active {
    background: var(--primary);
    border-color: var(--primary);
    color: var(--black);
    font-weight: 600;
  }

  .search-form {
    display: flex;
    gap: 0.5rem;
  }

  .search-form input {
    padding: 0.5rem 1rem;
    border: 2px solid var(--gray-200);
    border-radius: var(--radius);
    min-width: 200px;
    outline: none;
    transition: border-color 0.2s;
  }

  .search-form input:focus {
    border-color: var(--primary);
  }

  .loading, .empty {
    text-align: center;
    padding: 3rem;
    color: var(--gray-500);
  }

  .empty .btn {
    margin-top: 1rem;
  }

  .results-count {
    font-size: 0.85rem;
    color: var(--gray-500);
    margin-bottom: 1rem;
  }

  @media (max-width: 768px) {
    .filters {
      flex-direction: column;
      align-items: stretch;
    }
    .search-form {
      width: 100%;
    }
    .search-form input {
      flex: 1;
      min-width: 0;
    }
  }
</style>
