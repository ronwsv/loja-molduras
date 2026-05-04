<script lang="ts">
  import ProductCard from './ProductCard.svelte';

  interface Props {
    products: any[];
  }

  let { products }: Props = $props();
</script>

<div class="grid">
  {#each products as product (product.id)}
    <ProductCard {product} />
  {/each}
</div>

<style>
  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 1.5rem;
  }
</style>
