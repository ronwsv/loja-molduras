<script lang="ts">
  import { api } from '$lib/api';

  let current_password = $state('');
  let new_password = $state('');
  let confirm_password = $state('');
  let saving = $state(false);
  let success = $state(false);
  let error = $state('');

  async function save() {
    error = ''; success = false;
    if (new_password.length < 6) { error = 'A nova senha deve ter pelo menos 6 caracteres.'; return; }
    if (new_password !== confirm_password) { error = 'As senhas não coincidem.'; return; }
    saving = true;
    try {
      await api.changePassword({ current_password, new_password });
      success = true;
      current_password = new_password = confirm_password = '';
    } catch (err: any) {
      error = err.message;
    }
    saving = false;
  }
</script>

<svelte:head><title>Minha Conta - Admin</title></svelte:head>

<div class="page-header">
  <h1>Minha Conta</h1>
  <p>Altere sua senha de acesso ao painel</p>
</div>

<div class="card">
  <h2>Alterar Senha</h2>

  <label class="field-label">
    Senha atual
    <input type="password" bind:value={current_password} class="field-input" placeholder="Digite sua senha atual" />
  </label>

  <label class="field-label">
    Nova senha <span class="hint">(mínimo 6 caracteres)</span>
    <input type="password" bind:value={new_password} class="field-input" placeholder="Nova senha" />
  </label>

  <label class="field-label">
    Confirmar nova senha
    <input type="password" bind:value={confirm_password} class="field-input" placeholder="Repita a nova senha" />
  </label>

  {#if error}<p class="msg error">{error}</p>{/if}
  {#if success}<p class="msg success">Senha alterada com sucesso!</p>{/if}

  <button class="btn-primary" onclick={save} disabled={saving || !current_password || !new_password || !confirm_password}>
    {saving ? 'Salvando...' : 'Salvar nova senha'}
  </button>
</div>

<style>
  .page-header { margin-bottom: 2rem; }
  .page-header h1 { font-size: 1.6rem; margin: 0 0 0.25rem; color: #1a1a2e; }
  .page-header p { color: #666; margin: 0; }

  .card {
    background: #fff;
    border-radius: 10px;
    padding: 1.75rem;
    max-width: 420px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .card h2 { margin: 0 0 0.5rem; font-size: 1.1rem; color: #1a1a2e; }

  .field-label { display: flex; flex-direction: column; gap: 0.35rem; font-size: 0.85rem; font-weight: 600; color: #444; }
  .hint { font-weight: 400; color: #aaa; }
  .field-input { border: 1px solid #ddd; border-radius: 6px; padding: 0.6rem 0.75rem; font-size: 0.9rem; outline: none; transition: border 0.15s; }
  .field-input:focus { border-color: #2d6cdf; }

  .msg { margin: 0; font-size: 0.85rem; padding: 0.6rem 0.9rem; border-radius: 6px; }
  .msg.error { background: #fff0f0; color: #e74c3c; }
  .msg.success { background: #e8f8ee; color: #27ae60; }

  .btn-primary { background: #1a1a2e; color: #f5b800; border: none; border-radius: 8px; padding: 0.7rem 1.5rem; font-weight: 600; cursor: pointer; font-size: 0.9rem; transition: opacity 0.15s; align-self: flex-start; }
  .btn-primary:hover:not(:disabled) { opacity: 0.85; }
  .btn-primary:disabled { opacity: 0.45; cursor: not-allowed; }
</style>
