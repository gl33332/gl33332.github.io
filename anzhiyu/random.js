var posts=["2025/08/19/免费部署文生图AI/","2025/05/30/私信介绍/","2025/05/30/影视tv/","2025/06/01/Hexo-基础命令/"];function toRandomPost(){
    pjax.loadUrl('/'+posts[Math.floor(Math.random() * posts.length)]);
  };