<script lang="ts">
  import { goto } from '$app/navigation';
  import { authStore } from '$lib/stores';
  import { buildWhatsAppUrl } from '$lib/whatsapp';

  let searchQuery = $state('');
  let user: any = $state(null);
  const whatsappContactUrl = buildWhatsAppUrl();

  authStore.subscribe((s) => (user = s.user));

  function handleSearch(e: Event) {
    e.preventDefault();
    if (searchQuery.trim()) {
      goto(`/produtos?search=${encodeURIComponent(searchQuery.trim())}`);
    }
  }
</script>

<header class="header">
  <div class="header-top">
    <div class="container">
      <span>OS QUADROS MAIS PROCURADOS DA INTERNET!</span>
    </div>
  </div>

  <div class="header-main">
    <div class="container header-inner">
      <a href="/" class="logo">
        <div class="logo-icon">
          <span class="logo-nt">NT</span>
        </div>
        <div class="logo-text">
          <strong>MOLDURAS NOVO TEMPO</strong>
          <small>molduras & quadros</small>
        </div>
      </a>

      <form class="search-bar" onsubmit={handleSearch}>
        <input
          type="text"
          placeholder="O que você está buscando?"
          bind:value={searchQuery}
        />
        <button type="submit" class="search-btn" aria-label="Buscar produtos no catálogo">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
          </svg>
        </button>
      </form>

      <div class="header-actions">
        <a href="/contato" class="header-action">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
          </svg>
          <span>Atendimento</span>
        </a>

        {#if user?.is_admin}
          <a href="/admin" class="header-action admin-btn">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/>
              <rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>
            </svg>
            <span>Painel Admin</span>
          </a>
        {:else}
          <a href="/admin/login" class="header-action login-btn" title="Acesso admin">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/>
            </svg>
            <span>Admin</span>
          </a>
        {/if}

        <a href={whatsappContactUrl} target="_blank" rel="noopener noreferrer" class="header-action">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347"/>
          </svg>
          <span>Pedir no WhatsApp</span>
        </a>
      </div>
    </div>
  </div>
</header>

<style>
  .header-top {
    background: var(--primary);
    color: var(--black);
    text-align: center;
    padding: 0.4rem 0;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
  }

  .header-main {
    background: var(--black);
    padding: 1rem 0;
  }

  .header-inner {
    display: flex;
    align-items: center;
    gap: 2rem;
  }

  .logo {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    flex-shrink: 0;
  }

  .logo-icon {
    width: 50px;
    height: 50px;
    background: var(--primary);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .logo-nt {
    font-size: 1.4rem;
    font-weight: 800;
    color: var(--black);
    line-height: 1;
  }

  .logo-text {
    display: flex;
    flex-direction: column;
    color: var(--white);
  }

  .logo-text strong {
    font-size: 1.1rem;
    letter-spacing: 1px;
    line-height: 1.2;
  }

  .logo-text small {
    font-size: 0.7rem;
    color: var(--primary);
    text-transform: lowercase;
    letter-spacing: 0.5px;
  }

  .search-bar {
    flex: 1;
    display: flex;
    max-width: 500px;
    background: var(--white);
    border-radius: 50px;
    overflow: hidden;
  }

  .search-bar input {
    flex: 1;
    border: none;
    padding: 0.75rem 1.25rem;
    font-size: 0.9rem;
    outline: none;
    background: transparent;
  }

  .search-btn {
    padding: 0.75rem 1.25rem;
    color: var(--gray-500);
    transition: color 0.2s;
  }

  .search-btn:hover {
    color: var(--primary);
  }

  .header-actions {
    display: flex;
    gap: 1.5rem;
    flex-shrink: 0;
  }

  .header-action {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.25rem;
    color: var(--white);
    font-size: 0.7rem;
    transition: color 0.2s;
    position: relative;
  }

  .header-action:hover {
    color: var(--primary);
  }

  .admin-btn {
    color: var(--primary);
    border: 1px solid var(--primary);
    border-radius: 8px;
    padding: 0.35rem 0.75rem;
  }

  .admin-btn:hover {
    background: var(--primary);
    color: var(--black);
  }

  .login-btn {
    color: var(--gray-500);
    opacity: 0.5;
    font-size: 0.65rem;
  }

  .login-btn:hover {
    color: var(--white);
    opacity: 1;
  }

  @media (max-width: 768px) {
    .header-inner {
      flex-wrap: wrap;
      gap: 0.75rem;
    }
    .search-bar {
      order: 3;
      max-width: 100%;
      flex-basis: 100%;
    }
    .header-actions {
      gap: 1rem;
    }
    .header-action span {
      display: none;
    }
  }
</style>
