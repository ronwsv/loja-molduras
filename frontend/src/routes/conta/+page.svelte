<script lang="ts">
  import { goto } from '$app/navigation';
  import { authStore } from '$lib/stores';

  let mode = $state<'login' | 'register'>('login');
  let name = $state('');
  let email = $state('');
  let password = $state('');
  let phone = $state('');
  let error = $state('');
  let loading = $state(false);
  let user: any = $state(null);

  authStore.subscribe((s) => {
    user = s.user;
  });

  async function handleLogin(e: Event) {
    e.preventDefault();
    loading = true;
    error = '';
    try {
      await authStore.login(email, password);
      goto('/');
    } catch (e: any) {
      error = e.message;
    }
    loading = false;
  }

  async function handleRegister(e: Event) {
    e.preventDefault();
    loading = true;
    error = '';
    try {
      await authStore.register(name, email, password, phone);
      goto('/');
    } catch (e: any) {
      error = e.message;
    }
    loading = false;
  }

  function logout() {
    authStore.logout();
    goto('/');
  }
</script>

<svelte:head>
  <title>Minha Conta - Molduras Novo Tempo</title>
</svelte:head>

<section class="account-page">
  <div class="container">
    {#if user}
      <div class="profile-card">
        <div class="profile-header">
          <div class="avatar">
            <span>{user.name.charAt(0).toUpperCase()}</span>
          </div>
          <div>
            <h2>{user.name}</h2>
            <p>{user.email}</p>
          </div>
        </div>

        <div class="profile-links">
          <a href="/contato" class="profile-link">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
            </svg>
            Falar com atendimento
          </a>
          <button class="profile-link logout" onclick={logout}>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/>
            </svg>
            Sair da conta
          </button>
        </div>
      </div>
    {:else}
      <div class="auth-card">
        <div class="auth-tabs">
          <button class:active={mode === 'login'} onclick={() => mode = 'login'}>Entrar</button>
          <button class:active={mode === 'register'} onclick={() => mode = 'register'}>Criar conta</button>
        </div>

        {#if error}
          <p class="error-msg">{error}</p>
        {/if}

        {#if mode === 'login'}
          <form onsubmit={handleLogin}>
            <div class="form-group">
              <label for="email">Email</label>
              <input id="email" type="email" bind:value={email} required placeholder="seu@email.com" />
            </div>
            <div class="form-group">
              <label for="password">Senha</label>
              <input id="password" type="password" bind:value={password} required placeholder="Sua senha" />
            </div>
            <button type="submit" class="btn btn-primary btn-full" disabled={loading}>
              {loading ? 'Entrando...' : 'Entrar'}
            </button>
          </form>
        {:else}
          <form onsubmit={handleRegister}>
            <div class="form-group">
              <label for="name">Nome completo</label>
              <input id="name" type="text" bind:value={name} required placeholder="Seu nome" />
            </div>
            <div class="form-group">
              <label for="reg-email">Email</label>
              <input id="reg-email" type="email" bind:value={email} required placeholder="seu@email.com" />
            </div>
            <div class="form-group">
              <label for="phone">Telefone</label>
              <input id="phone" type="tel" bind:value={phone} placeholder="(11) 99999-9999" />
            </div>
            <div class="form-group">
              <label for="reg-password">Senha</label>
              <input id="reg-password" type="password" bind:value={password} required placeholder="Crie uma senha" minlength="6" />
            </div>
            <button type="submit" class="btn btn-primary btn-full" disabled={loading}>
              {loading ? 'Criando conta...' : 'Criar conta'}
            </button>
          </form>
        {/if}
      </div>
    {/if}
  </div>
</section>

<style>
  .account-page {
    padding: 3rem 0;
  }

  .auth-card, .profile-card {
    max-width: 450px;
    margin: 0 auto;
    background: var(--white);
    border: 1px solid var(--gray-200);
    border-radius: var(--radius-lg);
    padding: 2rem;
    box-shadow: var(--shadow);
  }

  .auth-tabs {
    display: flex;
    gap: 0;
    margin-bottom: 1.5rem;
    border-bottom: 2px solid var(--gray-200);
  }

  .auth-tabs button {
    flex: 1;
    padding: 0.75rem;
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--gray-500);
    border-bottom: 2px solid transparent;
    margin-bottom: -2px;
    transition: all 0.2s;
  }

  .auth-tabs button.active {
    color: var(--primary-dark);
    border-bottom-color: var(--primary);
  }

  .form-group {
    margin-bottom: 1rem;
  }

  .form-group label {
    display: block;
    font-size: 0.85rem;
    font-weight: 600;
    margin-bottom: 0.35rem;
    color: var(--gray-600);
  }

  .form-group input {
    width: 100%;
    padding: 0.7rem 1rem;
    border: 2px solid var(--gray-200);
    border-radius: var(--radius);
    outline: none;
    transition: border-color 0.2s;
  }

  .form-group input:focus {
    border-color: var(--primary);
  }

  .btn-full {
    width: 100%;
    margin-top: 0.5rem;
  }

  .error-msg {
    background: #fef2f2;
    color: var(--danger);
    padding: 0.75rem;
    border-radius: var(--radius);
    font-size: 0.85rem;
    margin-bottom: 1rem;
  }

  /* Profile */
  .profile-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.5rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--gray-200);
  }

  .avatar {
    width: 56px;
    height: 56px;
    background: var(--primary);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .avatar span {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--black);
  }

  .profile-header h2 {
    font-size: 1.2rem;
    margin-bottom: 0.1rem;
  }

  .profile-header p {
    font-size: 0.85rem;
    color: var(--gray-500);
  }

  .profile-links {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .profile-link {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem;
    border-radius: var(--radius);
    font-size: 0.9rem;
    font-weight: 500;
    color: var(--black);
    transition: background 0.2s;
    width: 100%;
    text-align: left;
  }

  .profile-link:hover {
    background: var(--gray-100);
  }

  .profile-link.logout {
    color: var(--danger);
    margin-top: 0.5rem;
    border-top: 1px solid var(--gray-200);
    padding-top: 1rem;
  }
</style>
