  # language: zh-CN
  功能: 元素定位方式不同


    场景: 元素的多种配置 01
    当 跳转到[locatorPage]
    当 页面渲染完成出现元素[元素1]
    那么 点击[元素1]
    而且 等待[3]秒
    那么 全屏截图


    场景: 元素的多种配置 02
    假如 跳转页面到[locatorPage]
    而且 页面渲染完成出现元素[元素1]
    那么 在[元素2]中向下查找[元素3]的元素


    场景: 文案的多种配置
    当 跳转到[locatorPage]
    当 页面渲染完成出现元素[元素1]
    而且 点击文案[文案1]
    而且 等待[3]秒
    那么 全屏截图





