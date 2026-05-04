<script lang="ts">
  let name = $state('');
  let email = $state('');
  let phone = $state('');
  let message = $state('');
  let sent = $state(false);

  function handleSubmit(e: Event) {
    e.preventDefault();
    sent = true;
    name = '';
    email = '';
    phone = '';
    message = '';
  }
</script>

<svelte:head>
  <title>Contato - Molduras Novo Tempo</title>
</svelte:head>

<section class="contact-page">
  <div class="container">
    <h1 class="section-title">Contato</h1>

    <div class="contact-layout">
      <div class="contact-info">
        <h2>Fale Conosco</h2>
        <p>Entre em contato conosco por um dos canais abaixo ou preencha o formulário.</p>

        <div class="info-items">
          <div class="info-item">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" stroke-width="2">
              <path d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
            </svg>
            <div>
              <strong>Telefone</strong>
              <p>(11) 99999-9999</p>
            </div>
          </div>
          <div class="info-item">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" stroke-width="2">
              <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/>
            </svg>
            <div>
              <strong>Email</strong>
              <p>contato@moldurasnovotempo.com.br</p>
            </div>
          </div>
          <div class="info-item">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" stroke-width="2">
              <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/>
            </svg>
            <div>
              <strong>Endereço</strong>
              <p>São Paulo - SP, Brasil</p>
            </div>
          </div>
        </div>

        <a
          href="https://wa.me/5511999999999?text=Olá! Vim pelo site e gostaria de mais informações."
          target="_blank"
          rel="noopener"
          class="btn btn-whatsapp"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
            <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
          </svg>
          Falar pelo WhatsApp
        </a>
      </div>

      <div class="contact-form">
        {#if sent}
          <div class="success-msg">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="var(--success)" stroke-width="2">
              <path d="M22 11.08V12a10 10 0 11-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>
            </svg>
            <h3>Mensagem enviada!</h3>
            <p>Entraremos em contato em breve.</p>
            <button class="btn btn-outline" onclick={() => sent = false}>Enviar outra mensagem</button>
          </div>
        {:else}
          <form onsubmit={handleSubmit}>
            <div class="form-group">
              <label for="name">Nome</label>
              <input id="name" type="text" bind:value={name} required placeholder="Seu nome" />
            </div>
            <div class="form-group">
              <label for="email">Email</label>
              <input id="email" type="email" bind:value={email} required placeholder="seu@email.com" />
            </div>
            <div class="form-group">
              <label for="phone">Telefone</label>
              <input id="phone" type="tel" bind:value={phone} placeholder="(11) 99999-9999" />
            </div>
            <div class="form-group">
              <label for="message">Mensagem</label>
              <textarea id="message" bind:value={message} rows="5" required placeholder="Como podemos ajudar?"></textarea>
            </div>
            <button type="submit" class="btn btn-primary btn-full">Enviar mensagem</button>
          </form>
        {/if}
      </div>
    </div>
  </div>
</section>

<style>
  .contact-page {
    padding: 3rem 0;
  }

  .contact-layout {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 3rem;
  }

  .contact-info h2 {
    font-size: 1.3rem;
    margin-bottom: 0.5rem;
  }

  .contact-info > p {
    color: var(--gray-500);
    font-size: 0.9rem;
    margin-bottom: 2rem;
  }

  .info-items {
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
    margin-bottom: 2rem;
  }

  .info-item {
    display: flex;
    gap: 0.75rem;
    align-items: flex-start;
  }

  .info-item strong {
    font-size: 0.9rem;
    display: block;
    margin-bottom: 0.1rem;
  }

  .info-item p {
    font-size: 0.85rem;
    color: var(--gray-600);
  }

  .btn-whatsapp {
    background: var(--green-whatsapp);
    color: white;
    padding: 0.75rem 1.5rem;
    border-radius: var(--radius);
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    transition: all 0.2s;
  }

  .btn-whatsapp:hover {
    background: #20bd5a;
    transform: translateY(-1px);
  }

  .contact-form {
    background: var(--gray-50);
    padding: 2rem;
    border-radius: var(--radius-lg);
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

  .form-group textarea {
    resize: vertical;
  }

  .btn-full {
    width: 100%;
  }

  .success-msg {
    text-align: center;
    padding: 2rem;
  }

  .success-msg h3 {
    margin: 1rem 0 0.5rem;
    font-size: 1.2rem;
  }

  .success-msg p {
    color: var(--gray-500);
    margin-bottom: 1.5rem;
  }

  @media (max-width: 768px) {
    .contact-layout {
      grid-template-columns: 1fr;
      gap: 2rem;
    }
  }
</style>
