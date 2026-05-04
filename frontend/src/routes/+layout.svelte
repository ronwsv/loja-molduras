<script lang="ts">
  import '../app.css';
  import Header from '$lib/components/Header.svelte';
  import Nav from '$lib/components/Nav.svelte';
  import Footer from '$lib/components/Footer.svelte';
  import WhatsAppButton from '$lib/components/WhatsAppButton.svelte';
  import CookieBanner from '$lib/components/CookieBanner.svelte';
  import { authStore } from '$lib/stores';
  import { onMount } from 'svelte';

  let { children } = $props();

  onMount(async () => {
    await authStore.init();
  });
</script>

<Header />
<Nav />
<main>
  {@render children()}
</main>
<Footer />
<WhatsAppButton />
<CookieBanner />
