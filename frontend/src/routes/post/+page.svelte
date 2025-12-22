<script lang="ts">
	import { onMount, getContext } from 'svelte';
	import { fade } from 'svelte/transition';
	import { resolve } from '$app/paths';
	import { goto } from '$app/navigation';
	import { api } from '$lib/api';
	import { USER_KEY, type UserState } from '$lib/user.svelte';
	import LoadingOverlay from '$lib/components/LoadingOverlay.svelte';

	const userState = getContext<UserState>(USER_KEY);
	let title = '';
	let content = '';
	let imageUrl = '';

	let isLoading = false;
	let activeTab: 'write' | 'preview' = 'write';
	let isNavigating = false;

	onMount(() => {
		if (!userState.isLoggedIn()) {
			goto('/login');
		}
	});

	async function handleSubmit() {
		if (!title || !content) {
			return;
		}

		isLoading = true;
		try {
			await api.posts.create({ title, content, owner_id: userState.current!.id });
			isNavigating = true;
			await goto('/');
		} catch (err) {
			console.error(err);
		} finally {
			isLoading = false;
		}
	}

	$: readTime = Math.ceil(content.length / 300);
</script>

{#if isNavigating}
	<LoadingOverlay message="文章發布成功，正在返回首頁..." />
{/if}

<div class="min-h-screen px-4 py-10 sm:px-6 lg:py-12">
	{#if userState.isLoggedIn()}
		<div class="mx-auto max-w-4xl" in:fade>
			<div class="mb-8 flex flex-col items-start justify-between gap-4 sm:flex-row sm:items-center">
				<div>
					<h1 class="text-3xl font-bold tracking-tight text-slate-900 dark:text-white">
						發表新文章
					</h1>

					<p class="mt-1 text-slate-500 dark:text-slate-400">分享您的知識與見解</p>
				</div>

				<div class="flex rounded-lg bg-slate-100 p-1 dark:bg-slate-800">
					<button
						on:click={() => (activeTab = 'write')}
						class="flex items-center gap-2 rounded-md px-4 py-2 text-sm font-medium transition-all
                        {activeTab === 'write'
							? 'bg-white text-blue-600 shadow-sm dark:bg-slate-700 dark:text-blue-400'
							: 'text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-200'}"
					>
						<svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
							/>
						</svg>
						編輯
					</button>

					<button
						on:click={() => (activeTab = 'preview')}
						class="flex items-center gap-2 rounded-md px-4 py-2 text-sm font-medium transition-all
						{activeTab === 'preview'
							? 'bg-white text-blue-600 shadow-sm dark:bg-slate-700 dark:text-blue-400'
							: 'text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-200'}"
					>
						<svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
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
						預覽
					</button>
				</div>
			</div>

			<div
				class="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-xl shadow-slate-200/50 dark:border-slate-800 dark:bg-slate-900 dark:shadow-slate-900/20"
			>
				{#if activeTab === 'write'}
					<form
						on:submit|preventDefault={handleSubmit}
						in:fade={{ duration: 200 }}
						class="flex flex-col gap-6 p-6 sm:p-8"
					>
						<div>
							<label for="title" class="sr-only">文章標題</label>

							<input
								type="text"
								id="title"
								bind:value={title}
								required
								placeholder="輸入文章標題..."
								class="w-full border-none bg-transparent p-0 text-3xl font-bold text-slate-900 placeholder-slate-300 focus:ring-0 dark:text-white dark:placeholder-slate-600"
							/>
						</div>

						<hr class="border-slate-100 dark:border-slate-800" />

						<div class="relative">
							<div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
								<svg
									class="h-5 w-5 text-slate-400"
									fill="none"
									viewBox="0 0 24 24"
									stroke="currentColor"
								>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
									/>
								</svg>
							</div>

							<input
								type="url"
								bind:value={imageUrl}
								placeholder="封面圖片網址 (選填)"
								class="block w-full rounded-lg border border-slate-200 bg-slate-50 py-2.5 pl-10 text-sm text-slate-900 focus:border-blue-500 focus:bg-white focus:ring-blue-500 dark:border-slate-700 dark:bg-slate-800 dark:text-white dark:focus:bg-slate-800"
							/>
						</div>

						<div class="relative">
							<textarea
								bind:value={content}
								required
								rows="12"
								placeholder="開始撰寫您的精彩內容..."
								class="block w-full resize-y rounded-lg border border-slate-200 bg-slate-50 p-4 text-base leading-relaxed text-slate-900 placeholder-slate-400 focus:border-blue-500 focus:bg-white focus:ring-blue-500 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-100 dark:focus:bg-slate-800"
							></textarea>

							<div class="absolute right-3 bottom-3 text-xs text-slate-400">
								{content.length} 字
							</div>
						</div>

						<div class="flex items-center justify-end gap-3 pt-2">
							<a
								href={resolve('/')}
								class="rounded-lg px-5 py-2.5 text-sm font-medium text-slate-600 transition-colors hover:bg-slate-100 hover:text-slate-900 dark:text-slate-400 dark:hover:bg-slate-800 dark:hover:text-white"
							>
								取消
							</a>

							<button
								type="submit"
								disabled={isLoading || !title || !content}
								class="inline-flex items-center gap-2 rounded-lg bg-blue-600 px-6 py-2.5 text-sm font-semibold text-white shadow-md shadow-blue-500/20 transition-all hover:bg-blue-700 hover:shadow-lg focus:ring-4 focus:ring-blue-500/30 disabled:cursor-not-allowed disabled:opacity-70"
							>
								{#if isLoading}
									<svg class="h-4 w-4 animate-spin" viewBox="0 0 24 24" fill="none">
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
									發布中...
								{:else}
									發布文章
								{/if}
							</button>
						</div>
					</form>
				{:else}
					<div in:fade={{ duration: 200 }} class="p-8 sm:p-10">
						<article class="prose prose-slate dark:prose-invert max-w-none">
							{#if imageUrl}
								<div class="mb-8 overflow-hidden rounded-xl">
									<img src={imageUrl} alt="Cover" class="h-64 w-full object-cover" />
								</div>
							{/if}

							<h1 class="mb-4 text-3xl font-bold text-slate-900 sm:text-4xl dark:text-white">
								{title || '無標題'}
							</h1>

							<div class="mb-8 flex items-center gap-4 text-sm text-slate-500 dark:text-slate-400">
								<span class="flex items-center gap-1">
									<svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											stroke-width="2"
											d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
										/>
									</svg>
									閱讀時間約 {readTime} 分鐘
								</span>
							</div>

							<div
								class="text-lg leading-relaxed whitespace-pre-wrap text-slate-700 dark:text-slate-300"
							>
								{content || '（無內容）'}
							</div>
						</article>
					</div>
				{/if}
			</div>
		</div>
	{/if}
</div>
