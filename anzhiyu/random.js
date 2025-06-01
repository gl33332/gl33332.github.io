var posts=["2025/05/30/私信介绍/","2025/06/01/Hexo-基础命令/","2025/06/02/影视tv/"];function toRandomPost(){
    pjax.loadUrl('/'+posts[Math.floor(Math.random() * posts.length)]);
  };