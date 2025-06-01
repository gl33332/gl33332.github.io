var posts=["source/_posts/","source/_posts/","source/_posts/"];function toRandomPost(){
    pjax.loadUrl('/'+posts[Math.floor(Math.random() * posts.length)]);
  };