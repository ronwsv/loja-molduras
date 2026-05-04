<script lang="ts">
  import { page } from '$app/state';
  import { onMount } from 'svelte';
  import { api } from '$lib/api';

  let categories: any[] = $state([]);
  let showDropdown = $state(false);
  let mobileOpen = $state(false);

  onMount(async () => {
    try {
      categories = await api.getCategories();
    } catch { /* ignore */ }
  });

  const links = [
    { href: '/', label: 'Início' },
    { href: '/sobre', label: 'Sobre nós' },
    { href: '/produtos', label: 'Catálogo', dropdown: true },
    { href: '/contato', label: 'Contato' },
    { href: '/comentarios', label: 'Comentários' },
    { href: '/produtos', label: 'Revenda' },
  ];
</script>

<nav class="nav">
  <div class="container nav-inner">
    <button class="mobile-toggle" onclick={() => mobileOpen = !mobileOpen}>
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        {#if mobileOpen}
          <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
        {:else}
          <line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/>
        {/if}
      </svg>
    </button>

    <ul class="nav-links" class:open={mobileOpen}>
      {#each links as link}
        <li
          class="nav-item"
          class:active={page.url.pathname === link.href}
          onmouseenter={() => link.dropdown && (showDropdown = true)}
          onmouseleave={() => link.dropdown && (showDropdown = false)}
        >
          <a href={link.href} onclick={() => mobileOpen = false}>
            {link.label}
            {#if link.dropdown}
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="6 9 12 15 18 9"/>
              </svg>
            {/if}
          </a>
          {#if link.dropdown && showDropdown}
            <div class="dropdown">
              <a href="/produtos" onclick={() => { showDropdown = false; mobileOpen = false; }}>Todos os Produtos</a>
              {#each categories as cat}
                <a href={`/produtos?category_id=${cat.id}`} onclick={() => { showDropdown = false; mobileOpen = false; }}>{cat.name}</a>
              {/each}
            </div>
          {/if}
        </li>
      {/each}
    </ul>
  </div>
</nav>

<style>
  .nav {
    background: var(--black-light);
    border-top: 1px solid rgba(255,255,255,0.05);
    position: sticky;
    top: 0;
    z-index: 100;
  }

  .nav-inner {
    display: flex;
    align-items: center;
  }

  .mobile-toggle {
    display: none;
    color: var(--white);
    padding: 0.75rem 0;
  }

  .nav-links {
    display: flex;
    list-style: none;
    gap: 0;
    width: 100%;
    justify-content: center;
  }

  .nav-item {
    position: relative;
  }

  .nav-item a {
    display: flex;
    align-items: center;
    gap: 0.25rem;
    padding: 0.9rem 1.25rem;
    color: var(--white);
    font-size: 0.9rem;
    font-weight: 500;
    transition: all 0.2s;
    white-space: nowrap;
  }

  .nav-item a:hover,
  .nav-item.active a {
    color: var(--primary);
  }

  .dropdown {
    position: absolute;
    top: 100%;
    left: 0;
    background: var(--black);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 0 0 var(--radius) var(--radius);
    min-width: 220px;
    box-shadow: var(--shadow-lg);
    z-index: 200;
  }

  .dropdown a {
    display: block;
    padding: 0.7rem 1.25rem;
    color: var(--white);
    font-size: 0.85rem;
    transition: all 0.15s;
  }

  .dropdown a:hover {
    background: var(--primary);
    color: var(--black);
  }

  @media (max-width: 768px) {
    .mobile-toggle {
      display: block;
    }
    .nav-links {
      display: none;
      flex-direction: column;
      position: absolute;
      top: 100%;
      left: 0;
      right: 0;
      background: var(--black);
      border-top: 1px solid rgba(255,255,255,0.1);
      z-index: 100;
    }
    .nav-links.open {
      display: flex;
    }
    .dropdown {
      position: static;
      border: none;
      border-radius: 0;
      box-shadow: none;
      background: var(--black-light);
    }
  }
</style>
