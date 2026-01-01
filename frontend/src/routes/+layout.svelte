<script lang="ts">
	import '../app.css';
	import { onMount, setContext } from 'svelte';
	import { fade } from 'svelte/transition';
	import { resolve } from '$app/paths';
	import { api } from '$lib/api';
	import { UserState, USER_KEY } from '$lib/user.svelte';

	let { children } = $props();
	const userState = new UserState();

	setContext(USER_KEY, userState);

	function handleLogout() {
		try {
			userState.logout();
		} catch (err) {
			console.error(err);
		}
	}

	onMount(async () => {
		try {
			const res = await api.user.me();

			userState.update(res.data);
		} catch (_err) {}
	});
</script>

<div
	class="flex min-h-screen flex-col bg-slate-50 font-sans text-slate-900 selection:bg-blue-500/20 dark:bg-slate-950 dark:text-slate-100"
>
	<div
		class="pointer-events-none fixed inset-0 z-0 opacity-[0.03] dark:opacity-[0.07]"
		style="background-image: url('data:image/svg+xml,%3Csvg width=\'60\' height=\'60\' viewBox=\'0 0 60 60\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cg fill=\'none\' fill-rule=\'evenodd\'%3E%3Cg fill=\'%239C92AC\' fill-opacity=\'1\'%3E%3Cpath d=\'M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z\'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E');"
	></div>
	<nav
		class="sticky top-0 z-50 w-full border-b border-slate-200/60 bg-white/70 backdrop-blur-xl dark:border-slate-800/60 dark:bg-slate-950/70"
	>
		<div class="mx-auto flex h-20 max-w-5xl items-center justify-between px-4 sm:px-6">
			<a href={resolve('/')} class="group flex items-center gap-3 outline-none">
				<div
					class="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-blue-600 to-indigo-700 text-white shadow-lg shadow-blue-500/20 transition-all duration-300 group-hover:scale-110 group-hover:rotate-3"
				>
					<span class="text-xl font-black">D</span>
				</div>
				<span class="text-2xl font-black tracking-tighter text-slate-800 dark:text-white">
					Dev<span class="text-blue-600">Blog</span>
				</span>
			</a>
			<div class="flex items-center gap-6">
				{#if userState.isLoggedIn()}
					<a
						href={resolve('/post')}
						class="hidden items-center gap-2 rounded-xl bg-slate-900 px-5 py-2 text-sm font-bold text-white transition-all hover:bg-blue-600 hover:shadow-xl hover:shadow-blue-500/20 sm:flex dark:bg-white dark:text-slate-900 dark:hover:bg-blue-500 dark:hover:text-white"
					>
						<svg
							class="h-4 w-4"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
							stroke-width="2.5"
						>
							<path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"></path>
						</svg>
						發表文章
					</a>
				{/if}

				<div class="h-8 w-px bg-slate-200 dark:bg-slate-800"></div>

				{#if userState.isLoggedIn()}
					<div class="flex items-center gap-4">
						<div
							class="flex items-center gap-3 rounded-full border border-slate-200 bg-white p-1 pr-4 shadow-sm transition hover:border-blue-300 dark:border-slate-800 dark:bg-slate-900"
						>
							<div
								class="flex h-8 w-8 items-center justify-center rounded-full bg-gradient-to-tr from-blue-500 to-indigo-600 text-xs font-black text-white"
							>
								{userState.current.username.substring(0, 1).toUpperCase()}
							</div>
							<span
								class="max-w-[100px] truncate text-sm font-bold text-slate-700 dark:text-slate-200"
							>
								{userState.current.username}
							</span>
						</div>
						<button
							onclick={handleLogout}
							class="group flex h-10 w-10 items-center justify-center rounded-xl text-slate-400 transition-all hover:bg-red-50 hover:text-red-600 dark:hover:bg-red-950/30"
							aria-label="登出"
						>
							<svg
								class="h-5 w-5 transition-transform group-hover:scale-110"
								fill="none"
								viewBox="0 0 24 24"
								stroke="currentColor"
								stroke-width="2"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
								></path>
							</svg>
						</button>
					</div>
				{:else}
					<nav class="flex items-center gap-4">
						<a
							href={resolve('/login')}
							class="text-sm font-bold text-slate-600 transition hover:text-blue-600 dark:text-slate-400 dark:hover:text-white"
						>
							登入
						</a>
						<a
							href={resolve('/register')}
							class="rounded-xl bg-blue-600 px-6 py-2 text-sm font-bold text-white shadow-lg shadow-blue-500/20 transition-all hover:-translate-y-0.5 hover:bg-blue-700"
						>
							註冊
						</a>
					</nav>
				{/if}
			</div>
		</div>
	</nav>
	<main class="relative z-10 mx-auto w-full max-w-5xl flex-1 px-4 py-12 sm:px-6 lg:py-16">
		<div in:fade={{ duration: 300 }}>{@render children()}</div>
	</main>
	<footer
		class="border-t border-slate-200/60 bg-white py-12 dark:border-slate-800/60 dark:bg-slate-950"
	>
		<div class="mx-auto max-w-5xl px-4 text-center sm:px-6">
			<p class="text-sm font-medium text-slate-500 dark:text-slate-400">
				© {new Date().getFullYear()} DevBlog
			</p>
		</div>
	</footer>
</div>
