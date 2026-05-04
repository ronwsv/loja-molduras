<script lang="ts">
  import { onMount } from 'svelte';
  import { api } from '$lib/api';

  let products: any[] = $state([]);
  let categories: any[] = $state([]);
  let loading = $state(true);
  let saving = $state(false);
  let error = $state('');

  // Modal state
  let showModal = $state(false);
  let editingProduct: any = $state(null);
  let form = $state({
    name: '', description: '',
    images: [] as string[], category_id: 0, featured: false,
  });
  let imageUrlInput = $state('');

  let uploadingImages = $state(false);

  // Delete confirm
  let deletingId: number | null = $state(null);

  let loadError = $state('');

  onMount(async () => {
    try {
      await loadData();
    } catch {
      loadError = 'Falha ao carregar dados. Verifique a conexão.';
    }
    loading = false;
  });

  async function loadData() {
    [products, categories] = await Promise.all([
      api.adminGetProducts(),
      api.adminGetCategories(),
    ]);
  }

  function openCreate() {
    editingProduct = null;
    form = { name: '', description: '', images: [], category_id: categories[0]?.id || 0, featured: false };
    imageUrlInput = '';
    error = '';
    showModal = true;
  }

  function openEdit(p: any) {
    editingProduct = p;
    form = {
      name: p.name, description: p.description,
      images: p.images?.map((i: any) => i.url) || (p.image_url ? [p.image_url] : []),
      category_id: p.category_id, featured: p.featured,
    };
    imageUrlInput = '';
    error = '';
    showModal = true;
  }

  async function saveProduct() {
    if (!form.name.trim() || !form.category_id) {
      error = 'Preencha nome e categoria.';
      return;
    }
    saving = true;
    error = '';
    try {
      const payload = { name: form.name, description: form.description, images: form.images, category_id: form.category_id, featured: form.featured };
      if (editingProduct) {
        await api.adminUpdateProduct(editingProduct.id, payload);
      } else {
        await api.adminCreateProduct(payload);
      }
      await loadData();
      showModal = false;
    } catch (e: any) {
      error = e.message || 'Erro ao salvar.';
    } finally {
      saving = false;
    }
  }

  async function handleImageUpload(e: Event) {
    const input = e.target as HTMLInputElement;
    const files = input.files;
    if (!files?.length) return;
    uploadingImages = true;
    try {
      for (const file of Array.from(files)) {
        const { url } = await api.uploadImage(file);
        form.images = [...form.images, url];
      }
    } catch (e: any) {
      error = e.message || 'Erro no upload das imagens.';
    } finally {
      uploadingImages = false;
      input.value = '';
    }
  }

  function removeImage(i: number) {
    form.images = form.images.filter((_: string, idx: number) => idx !== i);
  }

  function addImageFromUrl() {
    const url = imageUrlInput.trim();
    if (!url) return;
    try {
      const parsed = new URL(url);
      if (parsed.protocol !== 'http:' && parsed.protocol !== 'https:') {
        throw new Error('invalid protocol');
      }
      if (!form.images.includes(url)) {
        form.images = [...form.images, url];
      }
      imageUrlInput = '';
    } catch {
      error = 'URL de imagem invalida. Use http:// ou https://';
    }
  }

  async function confirmDelete(id: number) {
    try {
      await api.adminDeleteProduct(id);
      await loadData();
    } catch (e: any) {
      alert(e.message || 'Erro ao excluir produto.');
    }
    deletingId = null;
  }

  function categoryName(id: number) {
    return categories.find((c: any) => c.id === id)?.name || '—';
  }
</script>

<svelte:head><title>Produtos - Admin</title></svelte:head>

<div class="page-header">
  <div>
    <h1>Produtos</h1>
    <p>{products.length} produto{products.length !== 1 ? 's' : ''} cadastrado{products.length !== 1 ? 's' : ''}</p>
  </div>
  <button class="btn-primary" onclick={openCreate}>+ Novo Produto</button>
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
          <th>Categoria</th>
          <th>Destaque</th>
          <th>Ações</th>
        </tr>
      </thead>
      <tbody>
        {#each products as p (p.id)}
          <tr>
            <td>
              {#if p.image_url}
                <img src={p.image_url} alt={p.name} class="thumb" />
              {:else}
                <div class="thumb-placeholder">—</div>
              {/if}
            </td>
            <td class="name-cell">
              <span class="prod-name">{p.name}</span>
              {#if p.description}
                <span class="prod-desc">{p.description.slice(0, 60)}{p.description.length > 60 ? '…' : ''}</span>
              {/if}
            </td>
            <td>{categoryName(p.category_id)}</td>
            <td>
              <span class="badge" class:badge-yes={p.featured} class:badge-no={!p.featured}>
                {p.featured ? 'Sim' : 'Não'}
              </span>
            </td>
            <td class="actions">
              <button class="btn-edit" onclick={() => openEdit(p)}>Editar</button>
              {#if deletingId === p.id}
                <span class="confirm-row">
                  Excluir?
                  <button class="btn-danger-sm" onclick={() => confirmDelete(p.id)}>Sim</button>
                  <button class="btn-cancel-sm" onclick={() => deletingId = null}>Não</button>
                </span>
              {:else}
                <button class="btn-danger" onclick={() => deletingId = p.id}>Excluir</button>
              {/if}
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
{/if}

<!-- Modal -->
{#if showModal}
  <div class="overlay" role="dialog" aria-modal="true">
    <div class="modal">
      <div class="modal-header">
        <h2>{editingProduct ? 'Editar Produto' : 'Novo Produto'}</h2>
        <button class="close-btn" onclick={() => showModal = false}>✕</button>
      </div>
      <div class="modal-body">
        <div class="field">
          <label for="p-name">Nome *</label>
          <input id="p-name" type="text" bind:value={form.name} placeholder="Nome do produto" />
        </div>
        <div class="field">
          <label for="p-desc">Descrição</label>
          <textarea id="p-desc" rows="3" bind:value={form.description} placeholder="Descrição do produto"></textarea>
        </div>
        <div class="field">
          <label for="p-cat">Categoria *</label>
          <select id="p-cat" bind:value={form.category_id}>
            <option value={0} disabled>Selecione...</option>
            {#each categories as c}
              <option value={c.id}>{c.name}</option>
            {/each}
          </select>
        </div>
        <div class="field">
          <p class="field-section-title">Imagens do Produto</p>
          <div class="image-grid">
            {#each form.images as url, i}
              <div class="img-thumb">
                <img src={url} alt="imagem {i + 1}" />
                <button type="button" class="img-remove" onclick={() => removeImage(i)}>×</button>
              </div>
            {/each}
            <label class="img-add" class:uploading={uploadingImages}>
              {#if uploadingImages}
                <span class="upload-spinner">⏳</span>
              {:else}
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
                <span>Adicionar</span>
              {/if}
              <input type="file" accept="image/*" multiple onchange={handleImageUpload} style="display:none" disabled={uploadingImages} />
            </label>
          </div>
          <div class="url-input-row">
            <input
              type="url"
              bind:value={imageUrlInput}
              placeholder="https://..."
              onkeydown={(e) => e.key === 'Enter' && (e.preventDefault(), addImageFromUrl())}
            />
            <button type="button" class="btn-add-url" onclick={addImageFromUrl}>Adicionar URL</button>
          </div>
          <p class="field-hint">JPG, PNG ou WebP. Convertidas automaticamente para WebP. Primeira imagem = capa.</p>
        </div>
        <label class="checkbox-label">
          <input type="checkbox" bind:checked={form.featured} />
          Produto em destaque
        </label>
        {#if error}<p class="error-msg">{error}</p>{/if}
      </div>
      <div class="modal-footer">
        <button class="btn-cancel" onclick={() => showModal = false}>Cancelar</button>
        <button class="btn-primary" onclick={saveProduct} disabled={saving}>
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
  th { background: #f8f9fa; padding: 0.85rem 1rem; text-align: left; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.05em; color: #666; border-bottom: 1px solid #eee; white-space: nowrap; }
  td { padding: 0.75rem 1rem; border-bottom: 1px solid #f0f0f0; vertical-align: middle; }
  tr:last-child td { border-bottom: none; }
  tr:hover td { background: #fafafa; }

  .thumb { width: 48px; height: 48px; object-fit: cover; border-radius: 6px; }
  .thumb-placeholder { width: 48px; height: 48px; background: #eee; border-radius: 6px; display: flex; align-items: center; justify-content: center; color: #bbb; }

  .name-cell { max-width: 220px; }
  .prod-name { display: block; font-weight: 600; color: #1a1a2e; }
  .prod-desc { display: block; color: #888; font-size: 0.8rem; margin-top: 2px; }

  .badge { padding: 2px 8px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; }
  .badge-yes { background: #e8f8ee; color: #27ae60; }
  .badge-no { background: #f4f5f7; color: #aaa; }

  .actions { display: flex; align-items: center; gap: 0.4rem; white-space: nowrap; }

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
  .modal { background: #fff; border-radius: 12px; width: 100%; max-width: 520px; max-height: 90vh; overflow-y: auto; box-shadow: 0 8px 40px rgba(0,0,0,0.18); }
  .modal-header { display: flex; justify-content: space-between; align-items: center; padding: 1.25rem 1.5rem; border-bottom: 1px solid #eee; }
  .modal-header h2 { margin: 0; font-size: 1.1rem; color: #1a1a2e; }
  .close-btn { background: none; border: none; font-size: 1.1rem; cursor: pointer; color: #888; padding: 0.25rem; }
  .modal-body { padding: 1.25rem 1.5rem; display: flex; flex-direction: column; gap: 0.85rem; }
  .modal-footer { padding: 1rem 1.5rem; border-top: 1px solid #eee; display: flex; justify-content: flex-end; gap: 0.75rem; }

  .field { display: flex; flex-direction: column; gap: 0.3rem; }
  .field label { font-size: 0.82rem; font-weight: 600; color: #444; }
  .field input, .field select, .field textarea {
    padding: 0.55rem 0.8rem; border: 1.5px solid #ddd; border-radius: 7px;
    font-size: 0.9rem; font-family: inherit; resize: vertical;
  }
  .field input:focus, .field select:focus, .field textarea:focus { outline: none; border-color: #f5b800; }
  .field-section-title { font-size: 0.82rem; font-weight: 600; color: #444; margin: 0; }
  .checkbox-label { display: flex; align-items: center; gap: 0.5rem; font-size: 0.88rem; color: #444; cursor: pointer; }

  .btn-cancel { padding: 0.6rem 1.25rem; background: #f4f5f7; color: #555; border: none; border-radius: 8px; font-size: 0.9rem; font-weight: 600; cursor: pointer; }
  .btn-cancel:hover { background: #eee; }

  .error-msg { background: #fff0f0; color: #c0392b; border-radius: 6px; padding: 0.5rem 0.75rem; font-size: 0.83rem; margin: 0; }

  /* Image upload grid */
  .image-grid { display: flex; flex-wrap: wrap; gap: 0.6rem; margin-top: 0.25rem; }
  .img-thumb { position: relative; width: 80px; height: 80px; border-radius: 8px; overflow: hidden; border: 1.5px solid #ddd; flex-shrink: 0; }
  .img-thumb img { width: 100%; height: 100%; object-fit: cover; display: block; }
  .img-remove { position: absolute; top: 3px; right: 3px; background: rgba(0,0,0,0.65); color: #fff; border: none; border-radius: 50%; width: 20px; height: 20px; font-size: 0.85rem; cursor: pointer; display: flex; align-items: center; justify-content: center; line-height: 1; padding: 0; }
  .img-remove:hover { background: #c0392b; }
  .img-add { width: 80px; height: 80px; border-radius: 8px; border: 2px dashed #ddd; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 3px; cursor: pointer; color: #aaa; font-size: 0.7rem; font-weight: 600; transition: border-color 0.15s, color 0.15s; flex-shrink: 0; }
  .img-add:hover:not(.uploading) { border-color: #f5b800; color: #f5b800; }
  .img-add.uploading { opacity: 0.6; cursor: not-allowed; }
  .upload-spinner { font-size: 1.2rem; }
  .field-hint { font-size: 0.75rem; color: #aaa; margin: 0.3rem 0 0; }

  .url-input-row { display: flex; gap: 0.5rem; margin-top: 0.45rem; }
  .url-input-row input {
    flex: 1;
    padding: 0.55rem 0.8rem;
    border: 1.5px solid #ddd;
    border-radius: 7px;
    font-size: 0.85rem;
  }
  .url-input-row input:focus { outline: none; border-color: #f5b800; }
  .btn-add-url {
    padding: 0.5rem 0.8rem;
    border: none;
    border-radius: 7px;
    background: #e8f4ff;
    color: #2d6cdf;
    font-size: 0.8rem;
    font-weight: 600;
    cursor: pointer;
    white-space: nowrap;
  }
  .btn-add-url:hover { background: #d0e8ff; }
</style>
