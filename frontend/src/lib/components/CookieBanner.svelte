<script lang="ts">
  import { onMount } from 'svelte';

  let visible = $state(false);

  onMount(() => {
    if (!localStorage.getItem('cookies_accepted')) {
      visible = true;
    }
  });

  function accept() {
    localStorage.setItem('cookies_accepted', 'true');
    visible = false;
  }
</script>

{#if visible}
  <div class="cookie-banner">
    <p>
      Ao navegar por este site <strong>você aceita o uso de cookies</strong> para agilizar a sua experiência de compra.
    </p>
    <button class="btn btn-primary" onclick={accept}>ENTENDI</button>
  </div>
{/if}

<style>
  .cookie-banner {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: rgba(26, 26, 26, 0.95);
    color: var(--white);
    padding: 1rem 2rem;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1.5rem;
    z-index: 999;
    backdrop-filter: blur(10px);
  }

  .cookie-banner p {
    font-size: 0.85rem;
    text-align: center;
  }

  .cookie-banner strong {
    color: var(--primary);
  }

  .cookie-banner .btn {
    white-space: nowrap;
    padding: 0.5rem 1.5rem;
    font-size: 0.85rem;
  }
</style>
