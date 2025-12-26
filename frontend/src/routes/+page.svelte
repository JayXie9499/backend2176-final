<script lang="ts">
	import { fly, fade } from 'svelte/transition';

	let { data } = $props();
</script>

{#snippet dateDisplay(dateString: string)}
	<time
		datetime={dateString}
		class="flex items-center gap-1.5 text-xs font-semibold tracking-wide uppercase text-blue-600/80 dark:text-blue-400/80"
	>
		<svg class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
			<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
		</svg>
		{new Date(dateString).toLocaleDateString('zh-TW', {
			year: 'numeric',
			month: 'short',
			day: 'numeric'
		})}
	</time>
{/snippet}

<div class="mx-auto max-w-4xl px-4 py-12 sm:px-6 lg:py-20">
	<header class="mb-16 text-center sm:text-left">
		<h1 class="text-4xl font-extrabold tracking-tight text-slate-900 sm:text-5xl dark:text-white">
			最新文章
		</h1>
		<p class="mt-4 text-xl text-slate-600 dark:text-slate-400 font-medium">
			探索技術深度與設計美學的交匯點
		</p>
	</header>

	<div class="grid gap-10 sm:grid-cols-1">
		{#each data.data as post, i (post.id)}
			<article
				in:fly={{ y: 30, duration: 500, delay: i * 150 }}
				class="group relative flex flex-col overflow-hidden rounded-3xl border border-slate-200 bg-white p-8 shadow-sm transition-all duration-500
				hover:-translate-y-2 hover:border-blue-400/30 hover:shadow-2xl hover:shadow-blue-500/10
				dark:border-slate-800 dark:bg-slate-900 dark:hover:border-blue-500/30"
			>
				<div class="absolute -top-24 -right-24 h-64 w-64 rounded-full bg-blue-500/5 opacity-0 blur-3xl transition-opacity duration-700 group-hover:opacity-100 dark:bg-blue-400/10"></div>

				<div class="flex flex-col gap-5">
					<div class="flex items-center gap-4">
						{@render dateDisplay(post.created_at)}
						<span class="h-1 w-1 rounded-full bg-slate-300 dark:bg-slate-700"></span>
						<span class="text-xs font-bold uppercase tracking-widest text-slate-400">Technical</span>
					</div>

					<h2 class="text-3xl font-bold tracking-tight text-slate-900 dark:text-white">
						<a href={`/post/${post.id}`} class="before:absolute before:inset-0 focus:outline-none">
							<span class="bg-gradient-to-r from-blue-600 to-blue-600 bg-[length:0%_3px] bg-left-bottom bg-no-repeat transition-all duration-500 group-hover:bg-[length:100%_3px] dark:from-blue-400 dark:to-blue-400">
								{post.title}
							</span>
						</a>
					</h2>

					<p class="line-clamp-3 text-lg leading-relaxed text-slate-600 dark:text-slate-300/90">
						{post.content}
					</p>

					<div class="mt-4 flex items-center pt-6 border-t border-slate-100 dark:border-slate-800/50 text-sm font-bold text-blue-600 transition-colors group-hover:text-blue-500 dark:text-blue-400">
						<span class="relative overflow-hidden">
							閱讀全文
							<span class="absolute bottom-0 left-0 h-px w-full translate-x-[-105%] bg-current transition-transform duration-500 group-hover:translate-x-0"></span>
						</span>
						<svg class="ml-2 h-5 w-5 transition-transform duration-500 group-hover:translate-x-2" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M14 5l7 7m0 0l-7 7m7-7H3" />
						</svg>
					</div>
				</div>
			</article>
		{/each}
	</div>

	{#if data.data.length === 0}
		<div in:fade class="flex min-h-[400px] flex-col items-center justify-center rounded-3xl border-2 border-dashed border-slate-200 bg-slate-50/50 px-4 py-12 text-center dark:border-slate-800 dark:bg-slate-900/30">
			<div class="rounded-2xl bg-white p-6 shadow-sm dark:bg-slate-800">
				<svg class="h-12 w-12 text-slate-300 dark:text-slate-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z" />
				</svg>
			</div>
			<h3 class="mt-6 text-xl font-bold text-slate-900 dark:text-white">靜候內容更新</h3>
			<p class="mt-3 text-slate-500 dark:text-slate-400 max-w-xs">
				目前還沒有發布任何內容，請稍後再回來查看。
			</p>
		</div>
	{/if}
</div>