# Polytrack.best 图像资源

本目录包含Polytrack.best项目的所有图像资源和生成工具。

## 📁 文件说明

### 已创建的文件
- **`logo.svg`** - 品牌标识，低多边形风格的赛车轨道设计
- **`og-cover-generator.html`** - 社交分享图生成器 (1200x630像素)
- **`favicon-generator.html`** - 多尺寸favicon生成器

### 需要生成的文件
使用生成器创建以下文件：

#### 从 og-cover-generator.html 生成
- **`og-cover.jpg`** - 1200x630像素，用于社交媒体分享

#### 从 favicon-generator.html 生成
- **`favicon.ico`** - 标准网站图标
- **`favicon-16x16.png`** - 16x16像素PNG图标
- **`favicon-32x32.png`** - 32x32像素PNG图标
- **`apple-touch-icon.png`** - 180x180像素苹果设备图标

## 🎨 设计规范

### 品牌色彩
- **主色**: #0ea5e9 (天蓝色)
- **辅色**: #0284c7 (深蓝色)
- **强调色**: #0369a1 (深海蓝)

### 设计风格
- **低多边形**: 符合Polytrack游戏的视觉风格
- **几何图形**: 简洁的几何元素
- **赛车主题**: 轨道、速度线条等元素

## 🛠️ 使用说明

### 1. 生成社交分享图
1. 在浏览器中打开 `og-cover-generator.html`
2. 使用浏览器截图工具截取1200x630像素的图像
3. 保存为 `og-cover.jpg`

### 2. 生成Favicon
1. 在浏览器中打开 `favicon-generator.html`
2. 右键点击各个尺寸的图标，选择"另存为图像"
3. 保存为对应的文件名
4. 将16x16版本转换为 `favicon.ico` 格式

### 3. 在线转换工具推荐
- **ICO转换**: [favicon.io](https://favicon.io/)
- **图像优化**: [TinyPNG](https://tinypng.com/)
- **WebP转换**: [Squoosh](https://squoosh.app/)

## 📋 HTML集成

所有图像资源已在 `index.html` 中正确配置：

```html
<!-- Favicon配置 -->
<link rel="icon" type="image/x-icon" href="/favicon.ico">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">

<!-- Logo使用 -->
<img src="/assets/logo.svg" alt="Polytrack" class="h-6 w-6" />

<!-- 社交分享图 -->
<meta property="og:image" content="https://polytrack.best/assets/og-cover.jpg" />
```

## ✅ 完成检查清单

- [x] logo.svg 已创建
- [x] og-cover-generator.html 已创建
- [x] favicon-generator.html 已创建
- [x] HTML文件已更新图像路径
- [ ] og-cover.jpg 需要生成
- [ ] favicon.ico 需要生成
- [ ] 其他favicon尺寸需要生成

## 🎯 下一步

1. 使用生成器创建实际的图像文件
2. 测试所有图像在不同设备上的显示效果
3. 验证社交分享功能正常工作
4. 优化图像文件大小以提升性能

---

**创建日期**: 2025年1月12日  
**设计风格**: 低多边形赛车主题  
**品牌色彩**: 蓝色系渐变