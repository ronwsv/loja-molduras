<script lang="ts">
  import { get } from 'svelte/store';
  import { goto } from '$app/navigation';
  import { authStore } from '$lib/stores';

  let email = $state('');
  let password = $state('');
  let error = $state('');
  let loading = $state(false);

  async function handleLogin(e: Event) {
    e.preventDefault();
    error = '';
    loading = true;
    try {
      await authStore.login(email, password);
      const { user } = get(authStore);
      if (!user?.is_admin) {
        authStore.logout();
        error = 'Você não tem permissão de administrador.';
        return;
      }
      goto('/admin');
    } catch (err: any) {
      error = err.message || 'Credenciais inválidas.';
    } finally {
      loading = false;
    }
  }
</script>

<svelte:head><title>Login Admin - Molduras NT</title></svelte:head>

<div class="login-page">
  <div class="login-card">
    <div class="login-logo">
      <span class="logo-text">Admin</span>
      <span class="logo-sub">Molduras Novo Tempo</span>
    </div>
    <form onsubmit={handleLogin}>
      <div class="field">
        <label for="email">E-mail</label>
        <input id="email" type="email" bind:value={email} required placeholder="admin@exemplo.com" />
      </div>
      <div class="field">
        <label for="password">Senha</label>
        <input id="password" type="password" bind:value={password} required placeholder="••••••••" />
      </div>
      {#if error}
        <p class="error-msg">{error}</p>
      {/if}
      <button type="submit" class="btn-login" disabled={loading}>
        {loading ? 'Entrando...' : 'Entrar'}
      </button>
    </form>
  </div>
</div>

<style>
  :global(body) { margin: 0; }

  .login-page {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f4f5f7;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  }

  .login-card {
    background: #fff;
    border-radius: 12px;
    padding: 2.5rem 2rem;
    width: 100%;
    max-width: 380px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.08);
  }

  .login-logo {
    text-align: center;
    margin-bottom: 2rem;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .logo-text {
    font-size: 1.5rem;
    font-weight: 800;
    color: #f5b800;
    letter-spacing: 0.05em;
  }

  .logo-sub {
    font-size: 0.85rem;
    color: #888;
    margin-top: 4px;
  }

  .field {
    margin-bottom: 1rem;
  }

  label {
    display: block;
    font-size: 0.85rem;
    font-weight: 600;
    color: #444;
    margin-bottom: 0.35rem;
  }

  input {
    width: 100%;
    padding: 0.65rem 0.85rem;
    border: 1.5px solid #ddd;
    border-radius: 8px;
    font-size: 0.95rem;
    transition: border-color 0.2s;
    box-sizing: border-box;
  }

  input:focus {
    outline: none;
    border-color: #f5b800;
  }

  .error-msg {
    background: #fff0f0;
    color: #c0392b;
    border-radius: 6px;
    padding: 0.6rem 0.85rem;
    font-size: 0.85rem;
    margin-bottom: 1rem;
  }

  .btn-login {
    width: 100%;
    padding: 0.75rem;
    background: #f5b800;
    color: #1a1a1a;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 700;
    cursor: pointer;
    transition: opacity 0.2s;
  }

  .btn-login:disabled { opacity: 0.7; cursor: not-allowed; }
  .btn-login:hover:not(:disabled) { opacity: 0.9; }
</style>
