import axios from 'axios';

export function useSocial() {
  const tweetArticle = async (articleId: number) => {
    await axios.post(`/api/articles/${articleId}/publish`);  // In our API, publish already tweets if not tweeted before
  };
  const postInstagram = async (articleId: number) => {
    await axios.post(`/api/articles/${articleId}/publish`);  // Same as above, Instagram posting is part of publish
  };
  return { tweetArticle, postInstagram };
}
