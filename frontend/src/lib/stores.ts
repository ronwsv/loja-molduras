import { writable } from 'svelte/store';
import { api } from './api';

// Auth store
interface User {
  id: number;
  name: string;
  email: string;
  phone: string;
  address: string;
  is_admin: boolean;
}

function createAuthStore() {
  const { subscribe, set, update } = writable<{ user: User | null; token: string | null }>({
    user: null,
    token: null,
  });

  return {
    subscribe,
    init: async () => {
      if (typeof localStorage === 'undefined') return;
      const token = localStorage.getItem('token');
      if (token) {
        try {
          const user = await api.getMe();
          set({ user, token });
        } catch {
          localStorage.removeItem('token');
          set({ user: null, token: null });
        }
      }
    },
    login: async (email: string, password: string) => {
      const { access_token } = await api.login({ email, password });
      localStorage.setItem('token', access_token);
      const user = await api.getMe();
      set({ user, token: access_token });
    },
    register: async (name: string, email: string, password: string, phone: string = '') => {
      await api.register({ name, email, password, phone });
      const { access_token } = await api.login({ email, password });
      localStorage.setItem('token', access_token);
      const user = await api.getMe();
      set({ user, token: access_token });
    },
    logout: () => {
      localStorage.removeItem('token');
      set({ user: null, token: null });
    },
    setUser: (user: User) => update((s) => ({ ...s, user })),
  };
}

export const authStore = createAuthStore();
