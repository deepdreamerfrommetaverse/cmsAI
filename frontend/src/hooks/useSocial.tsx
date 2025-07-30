import api from "@/lib/api";

export function useSocial() {
  const tweetArticle = async (articleId: number) => {
    await api.post(`/api/social/twitter/${articleId}`);
  };
  const postInstagram = async (articleId: number) => {
    await api.post(`/api/social/instagram/${articleId}`);
  };
  return { tweetArticle, postInstagram };
}
