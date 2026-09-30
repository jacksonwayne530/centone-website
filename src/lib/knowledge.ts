import { getCollection, type CollectionEntry } from 'astro:content';

export type Article = CollectionEntry<'knowledge'>;

/** Published articles, newest first (drafts show up only in `astro dev`). */
export async function getArticles(): Promise<Article[]> {
  const all = await getCollection('knowledge', ({ data }) => import.meta.env.DEV || !data.draft);
  return all.sort((a, b) => b.data.date.getTime() - a.data.date.getTime() || a.data.order - b.data.order);
}

/** Rough reading time from the Markdown body, excluding the Sources footnotes. */
export function readingTime(article: Article): string {
  const text = (article.body ?? '').replace(/^\[\^[^\]]+\]:.*$/gm, '');
  const words = text.split(/\s+/).filter(Boolean).length;
  return `${Math.max(1, Math.round(words / 230))} min read`;
}

export function formatDate(date: Date): string {
  return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric', timeZone: 'UTC' });
}
