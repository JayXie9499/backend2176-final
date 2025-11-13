import { writable } from 'svelte/store';

const isBrowser = typeof window !== 'undefined';

const initialTheme = isBrowser ? localStorage.getItem('theme') || 'light' : 'light';

export const theme = writable<string>(initialTheme);

theme.subscribe((value) => {
	if (isBrowser) {
		localStorage.setItem('theme', value);
		const root = document.documentElement;
		if (value === 'dark') {
			root.classList.add('dark');
		} else {
			root.classList.remove('dark');
		}
	}
});
