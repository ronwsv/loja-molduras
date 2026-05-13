<script lang="ts">
  import { onMount } from 'svelte';
  import { api } from '$lib/api';

  let banners: any[] = $state([]);
  let loading = $state(true);
  let saving = $state(false);
  let error = $state('');
  let showModal = $state(false);
  let editingId: number | null = $state(null);
  let deleteId: number | null = $state(null);
  let uploadingImage = $state(false);

  const empty = () => ({ title: '', subtitle: '', text: '', cta: 'VER COLEÇÃO', image_url: '', sort_order: 0, active: true });
  let form: any = $state(empty());

  onMount(async () => {
    await load();
  });

  async function load() {
    loading = true;
    try { banners = await api.adminGetBanners(); } catch { /* ignore */ }
    loading = false;
  }

  function openCreate() {
    form = empty();
    editingId = null;
    error = '';
    showModal = true;
  }

  function openEdit(b: any) {
    form = { ...b };
    editingId = b.id;
    error = '';
    showModal = true;
  }

  async function handleImageUpload(e: Event) {
    const file = (e.target as HTMLInputElement).files?.[0];
    if (!file) return;
    uploadingImage = true;
    try {
      const res = await api.uploadImage(file);
      form.image_url = res.url;
    } catch (err: any) {
      error = err.message;
    }
    uploadingImage = false;
  }

  async function save() {
    if (!form.title.trim()) { error = 'Título obrigatório'; return; }
    saving = true; error = '';
    try {
      if (editingId) {
        await api.adminUpdateBanner(editingId, form);
      } else {
        await api.adminCreateBanner(form);
      }
      showModal = false;
      await load();
    } catch (err: any) {
      error = err.message;
    }
    saving = false;
  }

  async function confirmDelete() {
    if (!deleteId) return;
    try {
      await api.adminDeleteBanner(deleteId);
      await load();
    } catch { /* ignore */ }
    deleteId = null;
  }
</script>

<svelte:head><title>Banners - Admin</title></svelte:head>

<div class="page-header">
  <div>
    <h1>Banners do Hero</h1>
    <p>Gerencie os slides do banner principal da home. Tamanho recomendado: <strong>1400 × 500 px</strong></p>
  </div>
  <button class="btn-primary" onclick={openCreate}>+ Novo Banner</button>
</div>

{#if loading}
  <p class="loading">Carregando...</p>
{:else if banners.length === 0}
  <div class="empty">
    <p>Nenhum banner cadastrado. Os slides padrão estão sendo exibidos.</p>
    <button class="btn-primary" onclick={openCreate}>Criar primeiro banner</button>
  </div>
{:else}
  <div class="banner-list">
    {#each banners as b}
      <div class="banner-card" class:inactive={!b.active}>
        <div class="banner-preview" style="background-image: url('{b.image_url}')">
          {#if !b.image_url}<span class="no-img">Sem imagem</span>{/if}
          {#if !b.active}<span class="inactive-badge">Inativo</span>{/if}
        </div>
        <div class="banner-info">
          <div class="banner-texts">
            <strong>{b.title}</strong>
            {#if b.subtitle}<span class="subtitle">{b.subtitle}</span>{/if}
            {#if b.text}<p class="text">{b.text}</p>{/if}
          </div>
          <div class="banner-meta">
            <span class="cta-tag">CTA: {b.cta}</span>
            <span class="order-tag">Ordem: {b.sort_order}</span>
          </div>
          <div class="banner-actions">
            <button class="btn-edit" onclick={() => openEdit(b)}>Editar</button>
            <button class="btn-delete" onclick={() => deleteId = b.id}>Excluir</button>
          </div>
        </div>
      </div>
    {/each}
  </div>
{/if}

{#if showModal}
  <div class="overlay" onclick={() => showModal = false}>
    <div class="modal" onclick={(e) => e.stopPropagation()}>
      <h2>{editingId ? 'Editar Banner' : 'Novo Banner'}</h2>

      <div class="image-section">
        <label class="field-label">
          Imagem do banner
          <span class="size-hint">Tamanho recomendado: <strong>1400 × 500 px</strong> (proporção ~3:1) — JPG, PNG ou WebP, máx. 10MB</span>
        </label>
        {#if form.image_url}
          <div class="img-preview">
            <img src={form.image_url} alt="preview" />
            <button class="remove-img" onclick={() => form.image_url = ''}>✕</button>
          </div>
        {/if}
        <label class="upload-area">
          {#if uploadingImage}
            <span>Enviando...</span>
          {:else}
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
            <span>Clique para enviar imagem</span>
          {/if}
          <input type="file" accept="image/*" onchange={handleImageUpload} disabled={uploadingImage} />
        </label>
        <div class="or-divider">ou cole uma URL</div>
        <input type="url" placeholder="https://..." bind:value={form.image_url} class="field-input" />
      </div>

      <label class="field-label">
        Título <span class="required">*</span>
        <input type="text" placeholder="Ex: Molduras" bind:value={form.title} class="field-input" />
      </label>

      <label class="field-label">
        Subtítulo (em destaque)
        <input type="text" placeholder="Ex: PARA TODOS OS ESTILOS" bind:value={form.subtitle} class="field-input" />
      </label>

      <label class="field-label">
        Texto descritivo
        <input type="text" placeholder="Ex: Encontre a moldura perfeita..." bind:value={form.text} class="field-input" />
      </label>

      <label class="field-label">
        Texto do botão
        <input type="text" placeholder="Ex: VER COLEÇÃO" bind:value={form.cta} class="field-input" />
      </label>

      <div class="row-fields">
        <label class="field-label">
          Ordem de exibição
          <input type="number" min="0" bind:value={form.sort_order} class="field-input" />
        </label>
        <label class="field-label toggle-label">
          Ativo
          <input type="checkbox" bind:checked={form.active} />
        </label>
      </div>

      {#if error}<p class="field-error">{error}</p>{/if}

      <div class="modal-actions">
        <button class="btn-cancel" onclick={() => showModal = false}>Cancelar</button>
        <button class="btn-primary" onclick={save} disabled={saving}>
          {saving ? 'Salvando...' : 'Salvar'}
        </button>
      </div>
    </div>
  </div>
{/if}

{#if deleteId}
  <div class="overlay" onclick={() => deleteId = null}>
    <div class="modal confirm" onclick={(e) => e.stopPropagation()}>
      <h2>Excluir banner?</h2>
      <p>Esta ação não pode ser desfeita.</p>
      <div class="modal-actions">
        <button class="btn-cancel" onclick={() => deleteId = null}>Cancelar</button>
        <button class="btn-delete" onclick={confirmDelete}>Excluir</button>
      </div>
    </div>
  </div>
{/if}

<style>
  .page-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 2rem; gap: 1rem; }
  .page-header h1 { font-size: 1.6rem; margin: 0 0 0.25rem; color: #1a1a2e; }
  .page-header p { color: #666; margin: 0; font-size: 0.9rem; }
  .loading, .empty { color: #888; text-align: center; padding: 3rem; }
  .empty { display: flex; flex-direction: column; align-items: center; gap: 1rem; }

  .banner-list { display: flex; flex-direction: column; gap: 1rem; }

  .banner-card {
    display: flex;
    gap: 1rem;
    background: #fff;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  }
  .banner-card.inactive { opacity: 0.55; }

  .banner-preview {
    width: 240px;
    min-height: 90px;
    flex-shrink: 0;
    background: #eee center/cover no-repeat;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
  }
  .no-img { color: #aaa; font-size: 0.8rem; }
  .inactive-badge {
    position: absolute; top: 6px; left: 6px;
    background: rgba(0,0,0,0.6); color: #fff;
    font-size: 0.7rem; padding: 2px 6px; border-radius: 4px;
  }

  .banner-info { flex: 1; padding: 1rem; display: flex; flex-direction: column; gap: 0.5rem; }
  .banner-texts strong { font-size: 1rem; color: #1a1a2e; }
  .subtitle { font-size: 0.85rem; color: #f5b800; font-weight: 600; display: block; }
  .text { font-size: 0.8rem; color: #888; margin: 0; }
  .banner-meta { display: flex; gap: 0.75rem; }
  .cta-tag, .order-tag { font-size: 0.75rem; background: #f5f5f5; padding: 2px 8px; border-radius: 4px; color: #555; }
  .banner-actions { display: flex; gap: 0.5rem; margin-top: auto; }

  .btn-primary { background: #1a1a2e; color: #f5b800; border: none; border-radius: 8px; padding: 0.6rem 1.25rem; font-weight: 600; cursor: pointer; font-size: 0.9rem; transition: opacity 0.15s; }
  .btn-primary:hover:not(:disabled) { opacity: 0.85; }
  .btn-primary:disabled { opacity: 0.5; cursor: not-allowed; }
  .btn-edit { background: #e8f4ff; color: #2d6cdf; border: none; border-radius: 6px; padding: 0.4rem 0.9rem; font-size: 0.85rem; cursor: pointer; }
  .btn-delete { background: #fff0f0; color: #e74c3c; border: none; border-radius: 6px; padding: 0.4rem 0.9rem; font-size: 0.85rem; cursor: pointer; }
  .btn-cancel { background: #f0f0f0; color: #555; border: none; border-radius: 8px; padding: 0.6rem 1.25rem; font-size: 0.9rem; cursor: pointer; }

  .overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 1000; display: flex; align-items: center; justify-content: center; padding: 1rem; }
  .modal { background: #fff; border-radius: 12px; padding: 1.75rem; width: 100%; max-width: 560px; max-height: 90vh; overflow-y: auto; display: flex; flex-direction: column; gap: 1rem; }
  .modal.confirm { max-width: 380px; }
  .modal h2 { margin: 0; font-size: 1.2rem; color: #1a1a2e; }
  .modal-actions { display: flex; justify-content: flex-end; gap: 0.75rem; margin-top: 0.5rem; }

  .image-section { display: flex; flex-direction: column; gap: 0.5rem; }
  .field-label { display: flex; flex-direction: column; gap: 0.35rem; font-size: 0.85rem; font-weight: 600; color: #444; }
  .size-hint { font-weight: 400; color: #888; font-size: 0.8rem; }
  .field-input { border: 1px solid #ddd; border-radius: 6px; padding: 0.55rem 0.75rem; font-size: 0.9rem; outline: none; transition: border 0.15s; }
  .field-input:focus { border-color: #2d6cdf; }
  .field-error { color: #e74c3c; font-size: 0.85rem; margin: 0; }
  .required { color: #e74c3c; }

  .img-preview { position: relative; display: inline-block; }
  .img-preview img { width: 100%; max-height: 140px; object-fit: cover; border-radius: 6px; border: 1px solid #eee; }
  .remove-img { position: absolute; top: 4px; right: 4px; background: rgba(0,0,0,0.6); color: #fff; border: none; border-radius: 50%; width: 22px; height: 22px; font-size: 0.7rem; cursor: pointer; display: flex; align-items: center; justify-content: center; }

  .upload-area {
    border: 2px dashed #ddd; border-radius: 8px; padding: 1.25rem;
    display: flex; flex-direction: column; align-items: center; gap: 0.4rem;
    cursor: pointer; color: #888; font-size: 0.85rem; transition: border-color 0.15s;
  }
  .upload-area:hover { border-color: #2d6cdf; color: #2d6cdf; }
  .upload-area input { display: none; }

  .or-divider { text-align: center; color: #bbb; font-size: 0.8rem; }

  .row-fields { display: flex; gap: 1rem; }
  .row-fields .field-label { flex: 1; }
  .toggle-label { flex-direction: row !important; align-items: center; gap: 0.5rem; }
  .toggle-label input[type="checkbox"] { width: 18px; height: 18px; cursor: pointer; }
</style>
