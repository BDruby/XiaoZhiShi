// 博文卡片动画效果
document.addEventListener('DOMContentLoaded', function() {
    // 进入动画
    const postCards = document.querySelectorAll('.post-card');
    
    // 添加进入动画
    function addEntranceAnimation() {
        postCards.forEach((card, index) => {
            // 添加延迟类
            card.classList.add(`card-delay-${(index % 5) + 1}`);
            card.classList.add('fade-in-up');
            
            // 触发动画
            setTimeout(() => {
                card.classList.add('animate');
            }, 100);
        });
    }
    
    // 添加悬停涟漪效果
    function addRippleEffect() {
        postCards.forEach(card => {
            card.classList.add('interactive');
            
            card.addEventListener('click', function(e) {
                // 创建涟漪元素
                const ripple = document.createElement('span');
                ripple.classList.add('ripple');
                
                // 获取点击位置
                const rect = card.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                const x = e.clientX - rect.left - size / 2;
                const y = e.clientY - rect.top - size / 2;
                
                // 设置涟漪样式
                ripple.style.width = ripple.style.height = `${size}px`;
                ripple.style.left = `${x}px`;
                ripple.style.top = `${y}px`;
                
                // 添加到卡片中
                this.appendChild(ripple);
                
                // 移除涟漪元素
                setTimeout(() => {
                    ripple.remove();
                }, 600);
            });
        });
    }
    
    // 添加视差滚动效果
    function addParallaxEffect() {
        window.addEventListener('scroll', function() {
            const scrolled = window.scrollY;
            const rate = scrolled * -0.5;
            
            postCards.forEach(card => {
                const cardRect = card.getBoundingClientRect();
                const cardTop = cardRect.top + window.scrollY;
                
                // 只对可见的卡片应用效果
                if (cardTop - window.scrollY < window.innerHeight && cardTop + cardRect.height > window.scrollY) {
                    const parallaxRate = (scrolled - cardTop) * 0.1;
                    // 移除了图片的变换以避免与3D倾斜效果冲突
                }
            });
        });
    }
    
    // 添加浮动动画
    function addFloatingAnimation() {
        postCards.forEach((card, index) => {
            // 为每张卡片设置不同的动画延迟
            card.style.animationDelay = `${index * 0.1}s`;
        });
        
        // 添加浮动动画样式
        const style = document.createElement('style');
        style.textContent = `
            @keyframes float {
                0% { transform: translateY(0px); }
                50% { transform: translateY(-10px); }
                100% { transform: translateY(0px); }
            }
            
            .floating-cards .post-card {
                animation: float 3s ease-in-out infinite;
            }
        `;
        document.head.appendChild(style);
    }
    
    // 添加卡片悬停时的3D倾斜效果
    function addTiltEffect() {
        postCards.forEach(card => {
            card.addEventListener('mousemove', (e) => {
                const cardRect = card.getBoundingClientRect();
                const cardCenterX = cardRect.left + cardRect.width / 2;
                const cardCenterY = cardRect.top + cardRect.height / 2;
                
                const mouseX = e.clientX - cardCenterX;
                const mouseY = e.clientY - cardCenterY;
                
                const rotateY = mouseX / 20;
                const rotateX = -mouseY / 20;
                
                card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
            });
            
            card.addEventListener('mouseleave', () => {
                card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0)';
            });
        });
    }
    
    // 初始化所有效果
    addEntranceAnimation();
    addRippleEffect();
    addParallaxEffect();
    addTiltEffect();
    
    // 可选：添加浮动动画（如果需要）
    // addFloatingAnimation();
});

// 添加页面滚动进度指示器
document.addEventListener('DOMContentLoaded', function() {
    // 创建进度条元素
    const progressBar = document.createElement('div');
    progressBar.id = 'scroll-progress';
    progressBar.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 0%;
        height: 3px;
        background: linear-gradient(90deg, #4f46e5, #7c3aed, #ec4899);
        z-index: 9999;
        transition: width 0.1s ease;
    `;
    
    document.body.appendChild(progressBar);
    
    // 监听滚动事件
    window.addEventListener('scroll', function() {
        const scrollTop = window.scrollY;
        const docHeight = document.body.scrollHeight - window.innerHeight;
        const scrollPercent = (scrollTop / docHeight) * 100;
        
        progressBar.style.width = scrollPercent + '%';
    });
});

// 添加回到顶部按钮
document.addEventListener('DOMContentLoaded', function() {
    // 创建回到顶部按钮
    const backToTopButton = document.createElement('button');
    backToTopButton.id = 'back-to-top';
    backToTopButton.innerHTML = '↑';
    backToTopButton.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: #4f46e5;
        color: white;
        border: none;
        font-size: 20px;
        cursor: pointer;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        opacity: 0;
        transform: translateY(20px);
        transition: all 0.3s ease;
        z-index: 9998;
    `;
    
    document.body.appendChild(backToTopButton);
    
    // 监听滚动事件显示/隐藏按钮
    window.addEventListener('scroll', function() {
        if (window.scrollY > 300) {
            backToTopButton.style.opacity = '1';
            backToTopButton.style.transform = 'translateY(0)';
        } else {
            backToTopButton.style.opacity = '0';
            backToTopButton.style.transform = 'translateY(20px)';
        }
    });
    
    // 点击回到顶部
    backToTopButton.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    // 添加按钮悬停效果
    backToTopButton.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-3px) scale(1.1)';
        this.style.boxShadow = '0 6px 12px rgba(0, 0, 0, 0.15)';
    });
    
    backToTopButton.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0) scale(1)';
        this.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
    });
});

// 添加鼠标跟踪粒子效果
document.addEventListener('DOMContentLoaded', function() {
    // 创建粒子容器
    const particleContainer = document.createElement('div');
    particleContainer.id = 'particle-container';
    particleContainer.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 9997;
    `;
    
    document.body.appendChild(particleContainer);
    
    // 创建粒子
    function createParticle(x, y) {
        const particle = document.createElement('div');
        particle.classList.add('particle');
        
        // 随机颜色
        const colors = ['#4f46e5', '#7c3aed', '#ec4899', '#3b82f6', '#10b981'];
        const color = colors[Math.floor(Math.random() * colors.length)];
        
        particle.style.cssText = `
            position: absolute;
            width: 8px;
            height: 8px;
            background: ${color};
            border-radius: 50%;
            left: ${x}px;
            top: ${y}px;
            pointer-events: none;
            opacity: 0.7;
        `;
        
        particleContainer.appendChild(particle);
        
        // 随机动画
        const angle = Math.random() * Math.PI * 2;
        const speed = 2 + Math.random() * 3;
        const vx = Math.cos(angle) * speed;
        const vy = Math.sin(angle) * speed;
        
        // 动画
        let posX = x;
        let posY = y;
        let opacity = 0.7;
        let size = 8;
        
        const animate = () => {
            posX += vx;
            posY += vy;
            opacity -= 0.02;
            size -= 0.1;
            
            particle.style.left = `${posX}px`;
            particle.style.top = `${posY}px`;
            particle.style.opacity = opacity;
            particle.style.width = `${size}px`;
            particle.style.height = `${size}px`;
            
            if (opacity > 0 && size > 0) {
                requestAnimationFrame(animate);
            } else {
                particle.remove();
            }
        };
        
        animate();
    }
    
    // 鼠标移动时创建粒子
    let particleCount = 0;
    document.addEventListener('mousemove', function(e) {
        if (particleCount % 5 === 0) { // 每5次移动创建一个粒子
            createParticle(e.clientX, e.clientY);
        }
        particleCount++;
    });
});