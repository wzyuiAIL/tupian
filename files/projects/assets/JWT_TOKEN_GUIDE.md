# JWT Token 使用说明

## 问题说明

如果您在配置API时，Token以 `eyJ` 开头而不是 `pat_v2_` 开头，这是**完全正常的**！

## Coze支持两种Token格式

### 1. PAT格式（Personal Access Token）
```
pat_v2_xxxxxxxxxxxxxx_xxxxxxxxxxxxxx_xxxxxxxxxxxxxx_xxxxxxxxxxxxxx
```
- 以 `pat_v2_` 开头
- 这是个人访问令牌
- 用于个人工作流

### 2. JWT格式（JSON Web Token）
```
eyJhbGciOiJSUzI1NiIsImtpZCI6IjMxMWQwNzVjLTY2...
```
- 以 `eyJ` 开头
- 这是工作流访问令牌
- 用于工作流调用
- **您创建的就是这种格式！** ✅

## JWT格式特点

- **开头**: `eyJ`
- **结构**: 三个部分，用`.`分隔
  - Header（头部）
  - Payload（负载）
  - Signature（签名）
- **编码**: Base64编码
- **长度**: 通常比较长（200-1000字符）
- **安全性**: 每次创建都不同

## 示例

### 您的Token（JWT格式）
```
eyJhbGciOiJSUzI1NiIsImtpZCI6IjMxMWQwNzVjLTY2...
```

### PAT格式示例（仅供参考）
```
pat_v2_xxxxxxxxxxxxxx_xxxxxxxxxxxxxx_xxxxxxxxxxxxxx_xxxxxxxxxxxxxx
```

## 如何使用JWT Token

### 在调试工具中使用

1. 打开 `assets/api_debug.html`
2. 在"API Token"输入框中，粘贴您的JWT Token
3. 确保Token完整复制（以`eyJ`开头）
4. 点击"测试1：验证配置"
5. 系统会自动识别为JWT格式

### 在主HTML文件中使用

1. 打开 `assets/web_sdk_index.html`
2. 找到"API配置"区域
3. 在"请输入API Token"输入框中，粘贴您的JWT Token
4. 确保Token完整复制
5. 保存配置
6. 开始生成图片

## 常见问题

### Q: 我的Token以eyJ开头，是否正确？
**A**: ✅ 完全正确！JWT格式是Coze工作流的标准格式。

### Q: 为什么我的Token和示例不同？
**A**: JWT Token每次创建都不同，这是正常的。只要以`eyJ`开头，格式就是正确的。

### Q: Token太长，没有复制完怎么办？
**A**: 点击"复制API Token"按钮，会自动复制完整的Token。请确保完整复制。

### Q: Token可以重复使用吗？
**A**: JWT Token通常有有效期，如果过期需要重新创建。建议保存在安全的地方。

### Q: Token会过期吗？
**A**: 是的，JWT Token有有效期（通常是1-7天）。如果出现"Token无效"错误，需要重新创建。

## Token安全提示

- ✅ 妥善保存Token
- ✅ 不要分享给他人
- ✅ 不要提交到代码仓库
- ✅ 定期更换Token
- ❌ 不要在公开场合展示Token

## 下一步

配置好JWT Token后：

1. **测试连接**
   - 使用调试工具测试API连接
   - 确保API地址正确

2. **生成图片**
   - 上传2张产品图片
   - 选择风格
   - 点击生成

3. **下载结果**
   - 等待2-5分钟
   - 下载10张超高清图片

## 技术说明

### JWT结构解析

```
eyJhbGciOiJSUzI1NiIsImtpZCI6IjMxMWQwNzVjLTY2... . ... . ...
```

**第1部分（Header）**:
```json
{
  "alg": "RS256",
  "typ": "JWT"
}
```

**第2部分（Payload）**:
```json
{
  "sub": "user_id",
  "iat": 1234567890,
  "exp": 1234571490
}
```

**第3部分（Signature）**:
```
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  secret
)
```

## 总结

✅ **您的JWT Token格式完全正确！**

- Token以`eyJ`开头 ✅
- 这就是JWT格式 ✅
- 可以直接使用 ✅
- 无需任何转换 ✅

现在就使用您的JWT Token开始生成图片吧！🎉
