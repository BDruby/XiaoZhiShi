/**
 * 标签选择器组件
 * 提供可复用的标签选择功能
 */
class TagSelector {
    constructor(options) {
        this.options = {
            searchInput: '#tag-search',
            dropdown: '#tag-dropdown',
            selectedContainer: '#selected-tags',
            tagOption: '.tag-option',
            tagRemove: '.tag-remove',
            tagItem: '.tag-item',
            ...options
        };

        this.selectedTags = [];
        this.init();
    }

    init() {
        this.searchInput = document.querySelector(this.options.searchInput);
        this.dropdown = document.querySelector(this.options.dropdown);
        this.selectedContainer = document.querySelector(this.options.selectedContainer);

        if (!this.searchInput || !this.dropdown || !this.selectedContainer) {
            console.error('标签选择器初始化失败：缺少必要的DOM元素');
            return;
        }

        this.bindEvents();
        this.loadInitialTags();
    }

    bindEvents() {
        // 搜索框获得焦点时显示下拉框
        this.searchInput.addEventListener('focus', () => {
            this.updateTagOptions();
            this.dropdown.style.display = 'block';
        });

        // 搜索框失去焦点时隐藏下拉框（延迟以确保点击事件能触发）
        this.searchInput.addEventListener('blur', () => {
            setTimeout(() => {
                this.dropdown.style.display = 'none';
            }, 200);
        });

        // 搜索过滤
        this.searchInput.addEventListener('input', (e) => {
            this.filterTags(e.target.value);
        });

        // 键盘支持 - Enter键添加第一个匹配的标签
        this.searchInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                const visibleOptions = Array.from(this.dropdown.querySelectorAll(this.options.tagOption))
                    .filter(option => option.style.display !== 'none');

                if (visibleOptions.length > 0) {
                    const firstOption = visibleOptions[0];
                    const tagId = parseInt(firstOption.dataset.tagId);
                    const tagName = firstOption.dataset.tagName;
                    this.addTag(tagId, tagName);
                }
            }
        });

        // 点击标签选项
        this.dropdown.addEventListener('click', (e) => {
            const option = e.target.closest(this.options.tagOption);
            if (option) {
                const tagId = parseInt(option.dataset.tagId);
                const tagName = option.dataset.tagName;
                this.addTag(tagId, tagName);
            }
        });

        // 使用事件委托处理标签移除 - 改进版本
        this.selectedContainer.addEventListener('click', (e) => {
            const removeBtn = e.target.closest(this.options.tagRemove);
            if (removeBtn) {
                e.preventDefault();
                e.stopPropagation();
                const tagId = parseInt(removeBtn.dataset.tagId);
                if (!isNaN(tagId)) {
                    this.removeTag(tagId);
                }
            }
        });
    }

    loadInitialTags() {
        // 从已有的隐藏input获取初始标签
        const hiddenInputs = this.selectedContainer.querySelectorAll('input[name="tag_ids"]');
        hiddenInputs.forEach(input => {
            const tagId = parseInt(input.value);
            if (!this.selectedTags.includes(tagId)) {
                this.selectedTags.push(tagId);
            }
        });

        this.updateTagOptions();
    }

    addTag(tagId, tagName) {
        // 检查标签是否已经选择
        if (this.selectedTags.includes(tagId)) {
            return;
        }

        this.selectedTags.push(tagId);

        // 创建标签元素
        const tagElement = document.createElement('span');
        tagElement.className = 'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800 tag-item transition-all duration-200';
        tagElement.setAttribute('data-tag-id', tagId);

        tagElement.innerHTML = `
            ${tagName}
            <button type="button" class="flex-shrink-0 ml-1 h-4 w-4 rounded-full inline-flex items-center justify-center text-indigo-400 hover:bg-indigo-200 hover:text-indigo-500 focus:outline-none tag-remove transition-colors duration-150" data-tag-id="${tagId}">
                <span class="sr-only">移除标签</span>
                <svg class="h-3 w-3" stroke="currentColor" fill="none" viewBox="0 0 8 8">
                    <path stroke-linecap="round" stroke-width="1.5" d="M1 1l6 6m0-6L1 7" />
                </svg>
            </button>
            <input type="hidden" name="tag_ids" value="${tagId}">
        `;

        // 添加进入动画
        tagElement.style.transform = 'scale(0)';
        this.selectedContainer.appendChild(tagElement);

        // 触发重排，使初始状态生效
        tagElement.offsetHeight;
        tagElement.style.transform = 'scale(1)';

        // 更新标签选项状态
        this.updateTagOptions();

        // 清空搜索框
        this.searchInput.value = '';

        // 隐藏下拉框
        this.dropdown.style.display = 'none';
    }

    removeTag(tagId) {
        // 从数组中移除
        this.selectedTags = this.selectedTags.filter(id => id !== tagId);

        // 从DOM中移除标签元素 - 使用更精确的选择器
        const tagElement = this.selectedContainer.querySelector(`${this.options.tagItem}[data-tag-id="${tagId}"]`);

        if (tagElement) {
            // 添加移除动画效果
            tagElement.style.transition = 'all 0.3s ease';
            tagElement.style.transform = 'scale(0)';
            tagElement.style.opacity = '0';

            // 等待动画完成后再删除元素
            setTimeout(() => {
                if (tagElement.parentNode) {
                    tagElement.remove();
                }
            }, 300);
        } else {
            // 如果没找到元素（可能是因为动画还没结束用户又点了？或者选择器问题），尝试重新查找并强制移除
            // 这种情况很少见，但作为后备方案
            const fallbackElement = this.selectedContainer.querySelector(`[data-tag-id="${tagId}"]`);
            if (fallbackElement && fallbackElement.classList.contains(this.options.tagItem.substring(1))) {
                fallbackElement.remove();
            }
        }

        // 更新标签选项状态
        this.updateTagOptions();
    }

    filterTags(searchTerm) {
        const term = searchTerm.toLowerCase();
        const tagOptions = this.dropdown.querySelectorAll(this.options.tagOption);

        tagOptions.forEach(option => {
            const tagName = option.dataset.tagName.toLowerCase();
            const tagId = parseInt(option.dataset.tagId);
            const isAlreadySelected = this.selectedTags.includes(tagId);

            // 只有当标签未被选择且匹配搜索词时才显示
            if (!isAlreadySelected && tagName.includes(term)) {
                option.style.display = 'block';
            } else {
                option.style.display = 'none';
            }
        });
    }

    updateTagOptions() {
        const tagOptions = this.dropdown.querySelectorAll(this.options.tagOption);

        tagOptions.forEach(option => {
            const tagId = parseInt(option.dataset.tagId);
            if (this.selectedTags.includes(tagId)) {
                option.style.display = 'none'; // 隐藏已选择的标签
            } else {
                option.style.display = 'block'; // 显示未选择的标签
            }
        });
    }

    getSelectedTags() {
        return [...this.selectedTags];
    }

    clearTags() {
        this.selectedTags = [];
        const tagElements = this.selectedContainer.querySelectorAll(this.options.tagItem);
        tagElements.forEach(element => element.remove());
        this.updateTagOptions();
    }
}

// 导出类以供全局使用
window.TagSelector = TagSelector;