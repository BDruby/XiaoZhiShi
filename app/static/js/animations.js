// React Bits风格动画效果实现
document.addEventListener('DOMContentLoaded', function() {
  // 卡片进入动画 - 使用Intersection Observer
  const observerOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -50px 0px"
  };

  const cardObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry, index) => {
      if (entry.isIntersecting) {
        // 添加延迟效果
        setTimeout(() => {
          entry.target.classList.add('animate');
        }, index * 100);
      }
    });
  }, observerOptions);

  // 为所有卡片添加进入动画观察
  document.querySelectorAll('.post-card').forEach(card => {
    card.classList.add('fade-in-up');
    cardObserver.observe(card);
  });

  // 卡片涟漪效果
  document.querySelectorAll('.post-card').forEach(card => {
    card.addEventListener('click', function(e) {
      // 创建涟漪元素
      const ripple = document.createElement('span');
      ripple.classList.add('ripple');
      
      // 计算点击位置
      const rect = this.getBoundingClientRect();
      const size = Math.max(rect.width, rect.height);
      const x = e.clientX - rect.left - size / 2;
      const y = e.clientY - rect.top - size / 2;
      
      // 设置涟漪样式
      ripple.style.width = ripple.style.height = `${size}px`;
      ripple.style.left = `${x}px`;
      ripple.style.top = `${y}px`;
      
      // 添加涟漪到卡片
      this.appendChild(ripple);
      
      // 动画结束后移除涟漪
      setTimeout(() => {
        ripple.remove();
      }, 600);
    });
  });

  // 鼠标悬停时的微动画
  const cards = document.querySelectorAll('.post-card');
  cards.forEach(card => {
    card.addEventListener('mouseenter', function() {
      // 添加悬停时的额外效果
      const title = this.querySelector('.post-card-title');
      if (title) {
        title.style.transition = 'color 0.3s ease';
      }
    });

    card.addEventListener('mouseleave', function() {
      // 移除悬停效果
      const title = this.querySelector('.post-card-title');
      if (title) {
        title.style.color = '#1f2937';
      }
    });
  });

  // 页面滚动动画
  function animateOnScroll() {
    const elements = document.querySelectorAll('.post-card');
    elements.forEach(element => {
      const elementTop = element.getBoundingClientRect().top;
      const elementVisible = 150;

      if (elementTop < window.innerHeight - elementVisible) {
        element.classList.add('animate');
      }
    });
  }

  window.addEventListener('scroll', animateOnScroll);
  // 初始化页面加载时的动画
  setTimeout(animateOnScroll, 100);
});

// 实现React Bits风格的动画工具函数
const ReactBitsAnimations = {
  // 悬停缩放效果
  hoverScale: (selector, scale = 1.05) => {
    const elements = document.querySelectorAll(selector);
    elements.forEach(el => {
      el.addEventListener('mouseenter', () => {
        el.style.transform = `scale(${scale})`;
        el.style.transition = 'transform 0.3s ease';
      });
      
      el.addEventListener('mouseleave', () => {
        el.style.transform = 'scale(1)';
      });
    });
  },
  
  // 淡入效果
  fadeIn: (selector) => {
    const elements = document.querySelectorAll(selector);
    elements.forEach(el => {
      el.style.opacity = '0';
      el.style.transition = 'opacity 0.5s ease';
      
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
          }
        });
      });
      
      observer.observe(el);
    });
  },
  
  // 上滑进入效果
  slideUp: (selector) => {
    const elements = document.querySelectorAll(selector);
    elements.forEach((el, index) => {
      el.style.opacity = '0';
      el.style.transform = 'translateY(30px)';
      el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
      el.style.transitionDelay = `${index * 0.1}s`;
      
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
          }
        });
      });
      
      observer.observe(el);
    });
  },
  
  // 涟漪点击效果
  rippleClick: (selector) => {
    const elements = document.querySelectorAll(selector);
    elements.forEach(el => {
      el.style.position = 'relative';
      el.style.overflow = 'hidden';
      
      el.addEventListener('click', function(e) {
        // 创建涟漪元素
        const ripple = document.createElement('span');
        ripple.classList.add('ripple');
        
        // 计算点击位置
        const rect = this.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;
        
        // 设置涟漪样式
        ripple.style.width = ripple.style.height = `${size}px`;
        ripple.style.left = `${x}px`;
        ripple.style.top = `${y}px`;
        
        this.appendChild(ripple);
        
        // 动画结束后移除涟漪
        setTimeout(() => {
          ripple.remove();
        }, 600);
      });
    });
  },
  
  // 弹跳进入效果
  bounceIn: (selector) => {
    const elements = document.querySelectorAll(selector);
    elements.forEach((el, index) => {
      el.style.opacity = '0';
      el.style.transform = 'scale(0.3)';
      el.style.transition = 'all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55)';
      el.style.transitionDelay = `${index * 0.1}s`;
      
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'scale(1)';
          }
        });
      });
      
      observer.observe(el);
    });
  },
  
  // 旋转进入效果
  rotateIn: (selector) => {
    const elements = document.querySelectorAll(selector);
    elements.forEach((el, index) => {
      el.style.opacity = '0';
      el.style.transform = 'rotateY(90deg)';
      el.style.transition = 'all 0.6s ease';
      el.style.transitionDelay = `${index * 0.1}s`;
      
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'rotateY(0deg)';
          }
        });
      });
      
      observer.observe(el);
    });
  }
};

// 初始化特定动画效果
document.addEventListener('DOMContentLoaded', () => {
  // 为卡片应用滑动进入动画
  ReactBitsAnimations.slideUp('.post-card');
  
  // 为卡片应用涟漪点击效果
  ReactBitsAnimations.rippleClick('.post-card');
  
  // 为链接应用悬停效果
  ReactBitsAnimations.hoverScale('.post-card-link', 1.05);
  
  // 为标题应用弹跳进入效果
  ReactBitsAnimations.bounceIn('.post-card-title');
});