<script lang="ts">
  import { buildWhatsAppUrl } from '$lib/whatsapp';

  interface Props {
    product: {
      id: number;
      name: string;
      image_url: string;
      category?: { name: string };
    };
  }

  let { product }: Props = $props();

  const whatsappUrl = $derived(buildWhatsAppUrl(product.name));
</script>

<article class="card">
  <div class="card-image">
    <a href={`/produtos/${product.id}`} class="image-link" aria-label={`Ver detalhes de ${product.name}`}>
      <img src={product.image_url} alt={product.name} />
    </a>
    {#if product.category}
      <span class="card-category">{product.category.name}</span>
    {/if}
    <a
      href={whatsappUrl}
      target="_blank"
      rel="noopener noreferrer"
      class="whatsapp-btn"
      aria-label={`Tenho interesse em ${product.name}`}
    >
      Tenho interesse
    </a>
  </div>
  <div class="card-body">
    <h3 class="card-title"><a href={`/produtos/${product.id}`}>{product.name}</a></h3>
    <a href={`/produtos/${product.id}`} class="card-cta">Ver detalhes</a>
  </div>
</article>

<style>
  .card {
    background: var(--white);
    border: 1px solid var(--gray-200);
    border-radius: var(--radius-lg);
    overflow: hidden;
    transition: all 0.3s ease;
    display: flex;
    flex-direction: column;
  }

  .card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
    border-color: var(--primary);
  }

  .card-image {
    position: relative;
    aspect-ratio: 1;
    overflow: hidden;
    background: var(--gray-100);
  }

  .image-link {
    display: block;
    height: 100%;
  }

  .card-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.5s ease;
  }

  .card:hover .card-image img {
    transform: scale(1.05);
  }

  .card-category {
    position: absolute;
    top: 0.75rem;
    left: 0.75rem;
    background: var(--primary);
    color: var(--black);
    font-size: 0.7rem;
    font-weight: 600;
    padding: 0.25rem 0.75rem;
    border-radius: 50px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .card-body {
    padding: 1rem;
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
    flex: 1;
  }

  .card-title {
    font-size: 0.95rem;
    font-weight: 600;
    line-height: 1.3;
  }

  .card-title a {
    color: var(--black);
  }

  .card-cta {
    font-size: 0.8rem;
    color: var(--gray-500);
    margin-top: auto;
    padding-top: 0.5rem;
    border-top: 1px solid var(--gray-100);
    text-align: center;
    font-weight: 500;
    transition: color 0.2s;
  }

  .card:hover .card-cta {
    color: var(--primary-dark);
  }

  .whatsapp-btn {
    position: absolute;
    right: 0.65rem;
    bottom: 0.65rem;
    background: var(--green-whatsapp);
    color: var(--white);
    font-size: 0.75rem;
    font-weight: 700;
    padding: 0.45rem 0.75rem;
    border-radius: 50px;
    box-shadow: 0 6px 18px rgba(37, 211, 102, 0.4);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }

  .whatsapp-btn:hover {
    transform: translateY(-1px);
    box-shadow: 0 10px 22px rgba(37, 211, 102, 0.48);
  }
</style>
