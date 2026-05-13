<script lang="ts">
  import { onMount } from 'svelte';
  import { get } from 'svelte/store';
  import { goto } from '$app/navigation';
  import { page } from '$app/state';
  import { authStore } from '$lib/stores';

  let { children } = $props();
  let checking = $state(true);

  onMount(async () => {
    if ((page.url.pathname as string) === '/admin/login') {
      checking = false;
      return;
    }
    await authStore.init();
    const { user } = get(authStore);
    if (!user || !user.is_admin) {
      goto('/admin/login');
      return;
    }
    checking = false;
  });
</script>

{#if (page.url.pathname as string) === '/admin/login'}
  {@render children()}
{:else if checking}
  <div class="checking">Verificando acesso...</div>
{:else}
  <div class="admin-shell">
    <aside class="sidebar">
      <div class="sidebar-logo">
        <span class="logo-text">Admin</span>
        <span class="logo-sub">Molduras NT</span>
      </div>
      <nav class="sidebar-nav">
        <a href="/admin" class="nav-link" class:active={(page.url.pathname as string) === '/admin'}>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
          Dashboard
        </a>
        <a href="/admin/produtos" class="nav-link" class:active={(page.url.pathname as string).startsWith('/admin/produtos')}>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 01-8 0"/></svg>
          Produtos
        </a>
        <a href="/admin/categorias" class="nav-link" class:active={(page.url.pathname as string).startsWith('/admin/categorias')}>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 19a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h5l2 3h9a2 2 0 012 2z"/></svg>
          Categorias
        </a>
        <a href="/admin/banners" class="nav-link" class:active={(page.url.pathname as string).startsWith('/admin/banners')}>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="7" width="20" height="10" rx="2"/><path d="M16 3l4 4-4 4"/></svg>
          Banners
        </a>
      </nav>
      <div class="sidebar-footer">
        <a href="/admin/conta" class="nav-link" class:active={(page.url.pathname as string).startsWith('/admin/conta')}>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
          Minha Conta
        </a>
        <a href="/" class="nav-link" target="_blank">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
          Ver site
        </a>
        <button
          class="nav-link logout"
          onclick={() => { authStore.logout(); goto('/admin/login'); }}
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
          Sair
        </button>
      </div>
    </aside>
    <main class="admin-main">
      {@render children()}
    </main>
  </div>
{/if}

<style>
  :global(body) { margin: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }

  .checking {
    display: flex; align-items: center; justify-content: center;
    height: 100vh; color: #666; font-size: 1rem;
  }

  .admin-shell {
    display: flex;
    min-height: 100vh;
    background: #f4f5f7;
  }

  .sidebar {
    width: 220px;
    background: #1a1a2e;
    color: #ccc;
    display: flex;
    flex-direction: column;
    flex-shrink: 0;
    position: sticky;
    top: 0;
    height: 100vh;
  }

  .sidebar-logo {
    padding: 1.5rem 1.25rem 1rem;
    border-bottom: 1px solid #ffffff18;
    display: flex;
    flex-direction: column;
  }

  .logo-text {
    font-size: 1.1rem;
    font-weight: 700;
    color: #f5b800;
    letter-spacing: 0.05em;
  }

  .logo-sub {
    font-size: 0.75rem;
    color: #888;
    margin-top: 2px;
  }

  .sidebar-nav {
    flex: 1;
    padding: 1rem 0.75rem;
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  .nav-link {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    padding: 0.6rem 0.75rem;
    border-radius: 6px;
    font-size: 0.9rem;
    color: #aaa;
    text-decoration: none;
    transition: background 0.15s, color 0.15s;
    border: none;
    background: none;
    cursor: pointer;
    width: 100%;
    text-align: left;
  }

  .nav-link:hover, .nav-link.active {
    background: #ffffff14;
    color: #f5b800;
  }

  .nav-link.logout { color: #ff6b6b; }
  .nav-link.logout:hover { background: #ff6b6b18; color: #ff6b6b; }

  .sidebar-footer {
    padding: 0.75rem;
    border-top: 1px solid #ffffff18;
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  .admin-main {
    flex: 1;
    padding: 2rem;
    overflow-y: auto;
  }
</style>
