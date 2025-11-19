with open(r'D:\AIAPP\XiaoZhiShi\app\templates\admin\posts\edit.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        if '事件委托处理标签移除' in line or 'tag-remove' in line or 'selectedTagsContainer.addEventListener' in line:
            print(f'{i+1}:{line.strip()}')