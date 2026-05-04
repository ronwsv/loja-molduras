<script lang="ts">
  import { onMount } from 'svelte';
  import { api } from '$lib/api';

  let categories: any[] = $state([]);
  let loading = $state(true);
  let saving = $state(false);
  let error = $state('');

  let showModal = $state(false);
  let editingCat: any = $state(null);
  let form = $state({ name: '', image_url: '' });
  let deletingId: number | null = $state(null);
  let uploadingImage = $state(false);

  let loadError = $state('');

  onMount(async () => {
    try {
      await loadData();
    } catch {
      loadError = 'Falha ao carregar categorias. Verifique a conexão.';
    }
    loading = false;
  });

  async function loadData() {
    categories = await api.adminGetCategories();
  }

  function openCreate() {
    editingCat = null;
    form = { name: '', image_url: '' };
    error = '';
    showModal = true;
  }

  function openEdit(c: any) {
    editingCat = c;
    form = { name: c.name, image_url: c.image_url };
    error = '';
    showModal = true;
  }

  async function saveCategory() {
    if (!form.name.trim()) { error = 'Informe o nome da categoria.'; return; }
    saving = true;
    error = '';
    try {
      if (editingCat) {
        await api.adminUpdateCategory(editingCat.id, form);
      } else {
        await api.adminCreateCategory(form);
      }
      await loadData();
      showModal = false;
    } catch (e: any) {
      error = e.message || 'Erro ao salvar.';
    } finally {
      saving = false;
    }
  }

  async function handleCatImageUpload(e: Event) {
    const input = e.target as HTMLInputElement;
    const file = input.files?.[0];
    if (!file) return;
    uploadingImage = true;
    try {
      const { url } = await api.uploadImage(file);
      form.image_url = url;
    } catch (e: any) {
      error = e.message || 'Erro no upload da imagem.';
    } finally {
      uploadingImage = false;
      input.value = '';
    }
  }

  async function confirmDelete(id: number) {
    try {
      await api.adminDeleteCategory(id);
      await loadData();
    } catch (e: any) {
      alert(e.message || 'Erro ao excluir. Verifique se há produtos vinculados.');
    }
    deletingId = null;
  }
</script>

<svelte:head><title>Categorias - Admin</title></svelte:head>

<div class="page-header">
  <div>
    <h1>Categorias</h1>
    <p>{categories.length} categoria{categories.length !== 1 ? 's' : ''} cadastrada{categories.length !== 1 ? 's' : ''}</p>
  </div>
  <button class="btn-primary" onclick={openCreate}>+ Nova Categoria</button>
</div>

{#if loading}
  <p class="loading">Carregando...</p>
{:else if loadError}
  <p class="load-error">{loadError}</p>
{:else}
  <div class="table-wrap">
    <table>
      <thead>
        <tr>
          <th>Imagem</th>
          <th>Nome</th>
          <th>Slug</th>
          <th>Ações</th>
        </tr>
      </thead>
      <tbody>
        {#each categories as c (c.id)}
          <tr>
            <td>
              {#if c.image_url}
                <img src={c.image_url} alt={c.name} class="thumb" />
              {:else}
                <div class="thumb-placeholder">—</div>
              {/if}
            </td>
            <td class="cat-name">{c.name}</td>
            <td><code>{c.slug}</code></td>
            <td class="actions">
              <button class="btn-edit" onclick={() => openEdit(c)}>Editar</button>
              {#if deletingId === c.id}
                <span class="confirm-row">
                  Excluir?
                  <button class="btn-danger-sm" onclick={() => confirmDelete(c.id)}>Sim</button>
                  <button class="btn-cancel-sm" onclick={() => deletingId = null}>Não</button>
                </span>
              {:else}
                <button class="btn-danger" onclick={() => deletingId = c.id}>Excluir</button>
              {/if}
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
{/if}

{#if showModal}
  <div class="overlay" role="dialog" aria-modal="true">
    <div class="modal">
      <div class="modal-header">
        <h2>{editingCat ? 'Editar Categoria' : 'Nova Categoria'}</h2>
        <button class="close-btn" onclick={() => showModal = false}>✕</button>
      </div>
      <div class="modal-body">
        <div class="field">
          <label for="c-name">Nome *</label>
          <input id="c-name" type="text" bind:value={form.name} placeholder="Ex: Quadros Decorativos" />
        </div>
        <div class="field">
          <p class="field-section-title">Imagem da Categoria</p>
          <div class="cat-image-area">
            {#if form.image_url}
              <img src={form.image_url} alt="preview" class="cat-preview" />
            {/if}
            <div class="cat-image-btns">
              <label class="btn-upload" class:uploading={uploadingImage}>
                {uploadingImage ? 'Enviando...' : form.image_url ? 'Trocar imagem' : 'Escolher imagem'}
                <input type="file" accept="image/*" onchange={handleCatImageUpload} style="display:none" disabled={uploadingImage} />
              </label>
              {#if form.image_url}
                <button type="button" class="btn-remove-img" onclick={() => form.image_url = ''}>Remover</button>
              {/if}
            </div>
            <input
              type="url"
              bind:value={form.image_url}
              placeholder="Ou cole a URL da imagem (https://...)"
            />
            <p class="field-hint">JPG, PNG ou WebP. Convertida automaticamente para WebP.</p>
          </div>
        </div>
        {#if error}<p class="error-msg">{error}</p>{/if}
      </div>
      <div class="modal-footer">
        <button class="btn-cancel" onclick={() => showModal = false}>Cancelar</button>
        <button class="btn-primary" onclick={saveCategory} disabled={saving}>
          {saving ? 'Salvando...' : 'Salvar'}
        </button>
      </div>
    </div>
  </div>
{/if}

<style>
  .page-header {
    display: flex; justify-content: space-between; align-items: flex-start;
    margin-bottom: 1.5rem;
  }
  .page-header h1 { font-size: 1.6rem; margin: 0 0 0.25rem; color: #1a1a2e; }
  .page-header p { color: #888; margin: 0; font-size: 0.85rem; }
  .loading { color: #888; }
  .load-error { background: #fff0f0; color: #c0392b; padding: 1rem; border-radius: 8px; }

  .table-wrap { background: #fff; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); overflow: auto; }
  table { width: 100%; border-collapse: collapse; font-size: 0.88rem; }
  th { background: #f8f9fa; padding: 0.85rem 1rem; text-align: left; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.05em; color: #666; border-bottom: 1px solid #eee; }
  td { padding: 0.75rem 1rem; border-bottom: 1px solid #f0f0f0; vertical-align: middle; }
  tr:last-child td { border-bottom: none; }
  tr:hover td { background: #fafafa; }

  .thumb { width: 48px; height: 48px; object-fit: cover; border-radius: 6px; }
  .thumb-placeholder { width: 48px; height: 48px; background: #eee; border-radius: 6px; display: flex; align-items: center; justify-content: center; color: #bbb; }

  .cat-name { font-weight: 600; color: #1a1a2e; }
  code { font-size: 0.78rem; background: #f4f5f7; padding: 2px 6px; border-radius: 4px; color: #555; }

  .actions { display: flex; align-items: center; gap: 0.4rem; }
  .btn-primary { padding: 0.6rem 1.25rem; background: #1a1a2e; color: #f5b800; border: none; border-radius: 8px; font-size: 0.9rem; font-weight: 600; cursor: pointer; transition: opacity 0.15s; }
  .btn-primary:hover:not(:disabled) { opacity: 0.85; }
  .btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }

  .btn-edit { padding: 0.35rem 0.75rem; background: #e8f4ff; color: #2d6cdf; border: none; border-radius: 6px; font-size: 0.8rem; font-weight: 600; cursor: pointer; }
  .btn-edit:hover { background: #d0e8ff; }
  .btn-danger { padding: 0.35rem 0.75rem; background: #fff0f0; color: #c0392b; border: none; border-radius: 6px; font-size: 0.8rem; font-weight: 600; cursor: pointer; }
  .btn-danger:hover { background: #ffe0e0; }
  .confirm-row { display: flex; align-items: center; gap: 0.3rem; font-size: 0.8rem; color: #c0392b; font-weight: 600; }
  .btn-danger-sm { padding: 0.25rem 0.5rem; background: #c0392b; color: #fff; border: none; border-radius: 4px; font-size: 0.75rem; cursor: pointer; }
  .btn-cancel-sm { padding: 0.25rem 0.5rem; background: #eee; color: #555; border: none; border-radius: 4px; font-size: 0.75rem; cursor: pointer; }

  .overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.4); display: flex; align-items: center; justify-content: center; z-index: 1000; padding: 1rem; }
  .modal { background: #fff; border-radius: 12px; width: 100%; max-width: 420px; box-shadow: 0 8px 40px rgba(0,0,0,0.18); }
  .modal-header { display: flex; justify-content: space-between; align-items: center; padding: 1.25rem 1.5rem; border-bottom: 1px solid #eee; }
  .modal-header h2 { margin: 0; font-size: 1.1rem; color: #1a1a2e; }
  .close-btn { background: none; border: none; font-size: 1.1rem; cursor: pointer; color: #888; padding: 0.25rem; }
  .modal-body { padding: 1.25rem 1.5rem; display: flex; flex-direction: column; gap: 0.85rem; }
  .modal-footer { padding: 1rem 1.5rem; border-top: 1px solid #eee; display: flex; justify-content: flex-end; gap: 0.75rem; }

  .field { display: flex; flex-direction: column; gap: 0.3rem; }
  .field label { font-size: 0.82rem; font-weight: 600; color: #444; }
  .field-section-title { font-size: 0.82rem; font-weight: 600; color: #444; margin: 0; }
  .field input { padding: 0.55rem 0.8rem; border: 1.5px solid #ddd; border-radius: 7px; font-size: 0.9rem; }
  .field input:focus { outline: none; border-color: #f5b800; }

  .btn-cancel { padding: 0.6rem 1.25rem; background: #f4f5f7; color: #555; border: none; border-radius: 8px; font-size: 0.9rem; font-weight: 600; cursor: pointer; }
  .btn-cancel:hover { background: #eee; }
  .error-msg { background: #fff0f0; color: #c0392b; border-radius: 6px; padding: 0.5rem 0.75rem; font-size: 0.83rem; margin: 0; }

  /* Image upload */
  .cat-image-area { display: flex; flex-direction: column; gap: 0.5rem; }
  .cat-preview { width: 100%; max-height: 160px; object-fit: cover; border-radius: 8px; border: 1.5px solid #ddd; }
  .cat-image-btns { display: flex; gap: 0.5rem; }
  .btn-upload { display: inline-flex; align-items: center; justify-content: center; padding: 0.5rem 1rem; background: #e8f4ff; color: #2d6cdf; border-radius: 7px; font-size: 0.85rem; font-weight: 600; cursor: pointer; border: none; transition: background 0.15s; }
  .btn-upload:hover:not(.uploading) { background: #d0e8ff; }
  .btn-upload.uploading { opacity: 0.6; cursor: not-allowed; }
  .btn-remove-img { padding: 0.5rem 0.75rem; background: #fff0f0; color: #c0392b; border: none; border-radius: 7px; font-size: 0.85rem; font-weight: 600; cursor: pointer; }
  .btn-remove-img:hover { background: #ffe0e0; }
  .field-hint { font-size: 0.75rem; color: #aaa; margin: 0; }
</style>
