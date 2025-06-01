var posts=["2025/05/30/影视tv/","2025/05/30/私信介绍/","2025/06/02/Hexo-基础命令/","2025/06/02/测试/"];function toRandomPost(){
    pjax.loadUrl('/'+posts[Math.floor(Math.random() * posts.length)]);
  };