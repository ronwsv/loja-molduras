<script lang="ts">
  let reviews = $state([
    { id: 1, name: 'Maria Silva', rating: 5, comment: 'Quadros lindíssimos! Chegou super bem embalado e a qualidade é incrível. Recomendo demais!', date: '2025-01-15' },
    { id: 2, name: 'João Santos', rating: 5, comment: 'Comprei um kit de 3 quadros para a sala e ficou maravilhoso. Entrega rápida e produto de qualidade.', date: '2025-01-10' },
    { id: 3, name: 'Ana Oliveira', rating: 4, comment: 'Muito bom! As molduras são resistentes e o acabamento é perfeito. Voltarei a comprar com certeza.', date: '2024-12-20' },
    { id: 4, name: 'Pedro Costa', rating: 5, comment: 'Fiz um quadro personalizado com foto da família e ficou espetacular. Melhor presente que já dei!', date: '2024-12-15' },
    { id: 5, name: 'Carla Mendes', rating: 5, comment: 'Atendimento excelente pelo WhatsApp! Me ajudaram a escolher os quadros ideais para o escritório.', date: '2024-11-30' },
    { id: 6, name: 'Roberto Lima', rating: 4, comment: 'Boa variedade de produtos e preço justo. A placa decorativa ficou linda na barbearia.', date: '2024-11-20' },
  ]);

  let newReview = $state({ name: '', rating: 5, comment: '' });
  let showForm = $state(false);

  function submitReview(e: Event) {
    e.preventDefault();
    reviews = [
      { id: Date.now(), ...newReview, date: new Date().toISOString().split('T')[0] },
      ...reviews,
    ];
    newReview = { name: '', rating: 5, comment: '' };
    showForm = false;
  }

  function renderStars(rating: number) {
    return '★'.repeat(rating) + '☆'.repeat(5 - rating);
  }
</script>

<svelte:head>
  <title>Comentários - Molduras Novo Tempo</title>
</svelte:head>

<section class="reviews-page">
  <div class="container">
    <h1 class="section-title">Comentários dos Clientes</h1>

    <div class="reviews-header">
      <div class="rating-summary">
        <span class="big-rating">4.8</span>
        <div>
          <span class="stars">★★★★★</span>
          <p>{reviews.length} avaliações</p>
        </div>
      </div>
      <button class="btn btn-primary" onclick={() => showForm = !showForm}>
        {showForm ? 'Cancelar' : 'Deixar um comentário'}
      </button>
    </div>

    {#if showForm}
      <form class="review-form" onsubmit={submitReview}>
        <div class="form-group">
          <label for="name">Nome</label>
          <input id="name" type="text" bind:value={newReview.name} required placeholder="Seu nome" />
        </div>
        <div class="form-group">
          <label>Avaliação</label>
          <div class="star-select">
            {#each [1,2,3,4,5] as star}
              <button
                type="button"
                class="star-btn"
                class:active={newReview.rating >= star}
                onclick={() => newReview.rating = star}
              >★</button>
            {/each}
          </div>
        </div>
        <div class="form-group">
          <label for="comment">Comentário</label>
          <textarea id="comment" bind:value={newReview.comment} rows="4" required placeholder="Conte sua experiência..."></textarea>
        </div>
        <button type="submit" class="btn btn-primary">Enviar avaliação</button>
      </form>
    {/if}

    <div class="reviews-list">
      {#each reviews as review (review.id)}
        <div class="review-card">
          <div class="review-header">
            <div class="review-avatar">
              <span>{review.name.charAt(0)}</span>
            </div>
            <div>
              <h3>{review.name}</h3>
              <span class="review-date">{new Date(review.date).toLocaleDateString('pt-BR')}</span>
            </div>
            <span class="review-stars">{renderStars(review.rating)}</span>
          </div>
          <p class="review-text">{review.comment}</p>
        </div>
      {/each}
    </div>
  </div>
</section>

<style>
  .reviews-page {
    padding: 3rem 0;
  }

  .reviews-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--gray-200);
  }

  .rating-summary {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .big-rating {
    font-size: 3rem;
    font-weight: 800;
    color: var(--primary-dark);
  }

  .stars {
    color: var(--primary);
    font-size: 1.2rem;
  }

  .rating-summary p {
    font-size: 0.85rem;
    color: var(--gray-500);
  }

  .review-form {
    background: var(--gray-50);
    padding: 1.5rem;
    border-radius: var(--radius-lg);
    margin-bottom: 2rem;
    border: 1px solid var(--gray-200);
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

  .form-group input,
  .form-group textarea {
    width: 100%;
    padding: 0.7rem 1rem;
    border: 2px solid var(--gray-200);
    border-radius: var(--radius);
    outline: none;
    background: var(--white);
    transition: border-color 0.2s;
  }

  .form-group input:focus,
  .form-group textarea:focus {
    border-color: var(--primary);
  }

  .star-select {
    display: flex;
    gap: 0.25rem;
  }

  .star-btn {
    font-size: 1.5rem;
    color: var(--gray-300);
    transition: color 0.15s;
    padding: 0;
  }

  .star-btn.active {
    color: var(--primary);
  }

  .reviews-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .review-card {
    padding: 1.25rem;
    border: 1px solid var(--gray-200);
    border-radius: var(--radius-lg);
    transition: box-shadow 0.2s;
  }

  .review-card:hover {
    box-shadow: var(--shadow);
  }

  .review-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.75rem;
  }

  .review-avatar {
    width: 40px;
    height: 40px;
    background: var(--primary);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .review-avatar span {
    font-weight: 700;
    color: var(--black);
    font-size: 1.1rem;
  }

  .review-header h3 {
    font-size: 0.9rem;
    margin-bottom: 0.1rem;
  }

  .review-date {
    font-size: 0.75rem;
    color: var(--gray-400);
  }

  .review-stars {
    margin-left: auto;
    color: var(--primary);
    font-size: 1rem;
  }

  .review-text {
    color: var(--gray-600);
    font-size: 0.9rem;
    line-height: 1.6;
  }
</style>
