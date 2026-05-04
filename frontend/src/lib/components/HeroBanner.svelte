<script lang="ts">
  import { onMount } from 'svelte';

  const slides = [
    {
      title: 'Quadros',
      subtitle: 'SOB MEDIDA',
      text: 'Consulte-nos agora e transforme suas paredes com arte exclusiva!',
      cta: 'FALE CONOSCO',
      bg: 'https://placehold.co/1400x500/1a1a1a/F5B800?text=Quadros+Sob+Medida',
    },
    {
      title: 'Molduras',
      subtitle: 'PARA TODOS OS ESTILOS',
      text: 'Encontre a moldura perfeita para valorizar suas memórias e arte.',
      cta: 'VER COLEÇÃO',
      bg: 'https://placehold.co/1400x500/1a1a1a/F5B800?text=Molduras+Premium',
    },
    {
      title: 'Kits de Quadros',
      subtitle: 'DECORE SUA PAREDE',
      text: 'Kits prontos para montar a parede galeria dos seus sonhos!',
      cta: 'CONFIRA',
      bg: 'https://placehold.co/1400x500/1a1a1a/F5B800?text=Kits+de+Quadros',
    },
  ];

  let current = $state(0);
  let interval: ReturnType<typeof setInterval>;

  onMount(() => {
    interval = setInterval(() => {
      current = (current + 1) % slides.length;
    }, 5000);
    return () => clearInterval(interval);
  });

  function prev() {
    current = (current - 1 + slides.length) % slides.length;
  }
  function next() {
    current = (current + 1) % slides.length;
  }
</script>

<section class="hero">
  <div class="slides">
    {#each slides as slide, i}
      <div
        class="slide"
        class:active={i === current}
        style="background-image: url('{slide.bg}')"
      >
        <div class="slide-overlay"></div>
        <div class="slide-content">
          <h2 class="slide-title">{slide.title}</h2>
          <h1 class="slide-subtitle">{slide.subtitle}</h1>
          <p class="slide-text">{slide.text}</p>
          <a href="/produtos" class="slide-cta">{slide.cta}</a>
        </div>
      </div>
    {/each}
  </div>

  <button class="arrow arrow-left" onclick={prev}>
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <polyline points="15 18 9 12 15 6"/>
    </svg>
  </button>
  <button class="arrow arrow-right" onclick={next}>
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <polyline points="9 18 15 12 9 6"/>
    </svg>
  </button>

  <div class="dots">
    {#each slides as _, i}
      <button
        class="dot"
        class:active={i === current}
        onclick={() => current = i}
      ></button>
    {/each}
  </div>
</section>

<style>
  .hero {
    position: relative;
    height: 500px;
    overflow: hidden;
    background: var(--black);
  }

  .slides {
    width: 100%;
    height: 100%;
    position: relative;
  }

  .slide {
    position: absolute;
    inset: 0;
    background-size: cover;
    background-position: center;
    opacity: 0;
    transition: opacity 0.8s ease;
  }

  .slide.active {
    opacity: 1;
  }

  .slide-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(26,26,26,0.8) 0%, rgba(26,26,26,0.4) 100%);
  }

  .slide-content {
    position: relative;
    z-index: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    text-align: center;
    padding: 2rem;
  }

  .slide-title {
    font-family: var(--font-display);
    font-size: 2.5rem;
    color: var(--white);
    margin-bottom: 0.25rem;
  }

  .slide-subtitle {
    font-size: 3.5rem;
    font-weight: 800;
    color: var(--primary);
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 1rem;
  }

  .slide-text {
    color: var(--gray-300);
    font-size: 1.1rem;
    max-width: 500px;
    margin-bottom: 1.5rem;
    letter-spacing: 1px;
  }

  .slide-cta {
    display: inline-block;
    background: var(--primary);
    color: var(--black);
    padding: 0.9rem 2.5rem;
    font-weight: 700;
    font-size: 1rem;
    border-radius: 50px;
    letter-spacing: 1px;
    transition: all 0.3s;
  }

  .slide-cta:hover {
    background: var(--primary-dark);
    transform: scale(1.05);
  }

  .arrow {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    z-index: 10;
    width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    color: var(--white);
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.2);
    transition: all 0.2s;
  }

  .arrow:hover {
    background: var(--primary);
    color: var(--black);
    border-color: var(--primary);
  }

  .arrow-left { left: 1rem; }
  .arrow-right { right: 1rem; }

  .dots {
    position: absolute;
    bottom: 1.5rem;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    gap: 0.5rem;
    z-index: 10;
  }

  .dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: rgba(255,255,255,0.4);
    transition: all 0.2s;
  }

  .dot.active {
    background: var(--primary);
    transform: scale(1.3);
  }

  @media (max-width: 768px) {
    .hero {
      height: 350px;
    }
    .slide-title {
      font-size: 1.5rem;
    }
    .slide-subtitle {
      font-size: 2rem;
      letter-spacing: 2px;
    }
    .slide-text {
      font-size: 0.9rem;
    }
  }
</style>
