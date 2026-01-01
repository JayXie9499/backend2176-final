<script lang="ts">
	import { onMount, getContext } from 'svelte';
	import { fly } from 'svelte/transition';
	import { resolve } from '$app/paths';
	import { goto } from '$app/navigation';
	import { api } from '$lib/api';
	import { USER_KEY, type UserState } from '$lib/user.svelte';
	import LoadingOverlay from '$lib/components/LoadingOverlay.svelte';

	const userState = getContext<UserState>(USER_KEY);
	let username = $state('');
	let password = $state('');
	let showPassword = $state(false);
	let isLoading = $state(false);
	let isNavigating = $state(false);

	async function handleSubmit(e: Event) {
		e.preventDefault();

		if (!username || !password) {
			return;
		}

		isLoading = true;
		try {
			const res = await api.auth.login({ username, password });

			userState.update(res.data);
			isNavigating = true;
			await goto('/');
		} catch (err) {
			console.error(err);
		} finally {
			isLoading = false;
		}
	}

	onMount(() => {
		if (userState.isLoggedIn()) {
			goto('/');
		}
	});
</script>

{#if isNavigating}
	<LoadingOverlay message="登入成功，正在跳轉..." />
{/if}

<div class="flex min-h-[85vh] items-center justify-center px-4 py-12">
	<div
		in:fly={{ y: 20, duration: 400 }}
		class="w-full max-w-md overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-xl shadow-slate-200/50 dark:border-slate-800 dark:bg-slate-900 dark:shadow-slate-900/50"
	>
		<div class="p-8 sm:p-10">
			<div class="mb-8 text-center">
				<h1 class="text-3xl font-bold tracking-tight text-slate-900 dark:text-white">歡迎回來</h1>
				<p class="mt-2 text-sm text-slate-500 dark:text-slate-400">請輸入您的帳號密碼以繼續</p>
			</div>

			<form class="flex flex-col gap-6" onsubmit={handleSubmit}>
				<div>
					<label
						for="username"
						class="mb-1.5 block text-sm font-semibold text-slate-700 dark:text-slate-300"
					>
						使用者名稱
					</label>
					<div class="relative">
						<div
							class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3 text-slate-400"
						>
							<svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
								/>
							</svg>
						</div>
						<input
							type="text"
							id="username"
							bind:value={username}
							required
							placeholder="請輸入使用者名稱"
							class="block w-full rounded-lg border border-slate-300 bg-white py-2.5 pl-10 text-slate-900 placeholder-slate-400 transition-all focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10 focus:outline-none dark:border-slate-700 dark:bg-slate-800 dark:text-white dark:focus:ring-blue-500/20"
						/>
					</div>
				</div>

				<div>
					<label
						for="password"
						class="mb-1.5 block text-sm font-semibold text-slate-700 dark:text-slate-300"
					>
						密碼
					</label>
					<div class="relative">
						<div
							class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3 text-slate-400"
						>
							<svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
								/>
							</svg>
						</div>
						<input
							type={showPassword ? 'text' : 'password'}
							id="password"
							bind:value={password}
							required
							placeholder="••••••••"
							class="block w-full rounded-lg border border-slate-300 bg-white py-2.5 pr-10 pl-10 text-slate-900 placeholder-slate-400 transition-all focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10 focus:outline-none dark:border-slate-700 dark:bg-slate-800 dark:text-white dark:focus:ring-blue-500/20"
						/>
						<button
							type="button"
							onclick={() => (showPassword = !showPassword)}
							class="absolute inset-y-0 right-0 flex items-center pr-3 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
						>
							{#if showPassword}
								<svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"
									/>
								</svg>
							{:else}
								<svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
									/>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
									/>
								</svg>
							{/if}
						</button>
					</div>
				</div>

				<button
					type="submit"
					disabled={isLoading}
					class="mt-2 flex w-full items-center justify-center rounded-lg bg-blue-600 px-4 py-2.5 text-base font-bold text-white shadow-md shadow-blue-500/20 transition-all hover:bg-blue-700 hover:shadow-lg focus:ring-4 focus:ring-blue-500/50 focus:outline-none disabled:cursor-not-allowed disabled:opacity-70"
				>
					{#if isLoading}
						<svg
							class="mr-3 h-5 w-5 animate-spin text-white"
							xmlns="http://www.w3.org/2000/svg"
							fill="none"
							viewBox="0 0 24 24"
						>
							<circle
								class="opacity-25"
								cx="12"
								cy="12"
								r="10"
								stroke="currentColor"
								stroke-width="4"
							/>
							<path
								class="opacity-75"
								fill="currentColor"
								d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
							/>
						</svg>
						登入中...
					{:else}
						立即登入
					{/if}
				</button>
			</form>

			<p class="mt-8 text-center text-sm text-slate-500 dark:text-slate-400">
				還沒有帳號？
				<a
					href={resolve('/register')}
					class="font-semibold text-blue-600 transition hover:text-blue-500 hover:underline dark:text-blue-400"
				>
					免費註冊
				</a>
			</p>
		</div>
	</div>
</div>
