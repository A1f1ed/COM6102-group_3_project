<template>
	<view class="customer-service">
		<!-- 顶部导航栏 -->
				
		<view class="nav">
			<view class="nav-left" @click="back">
				<view class="back">
					<text class="icon-back">←</text>
				</view>
				<view class="back-text">
					返回
				</view>
			</view>
			<text class="title">智能客服</text>
			<view class="nav-right">
				<!-- 添加删除按钮 -->
				<view class="clear-btn" @click="showClearConfirm">
					<text class="icon-delete">🗑️</text>
				</view>
				<view class="mode-switch" @click="toggleMode">
					<text>{{ isAIMode ? '快速客服' : 'AI客服' }}</text>
				</view>
			</view>
		</view>

		<!-- 聊天区域 -->
		<view class="chat-area">
			<scroll-view scroll-y="true" class="message-list" :scroll-top="scrollTop"
				:scroll-with-animation="scrollAnimation">
				<view class="message-item" v-for="(item, index) in messages" :key="index"
					:class="{'user-message': item.role === 'user', 'bot-message': item.role === 'assistant'}">
					<view class="message-content">
						{{item.content}}
					</view>
				</view>
				<view class="loading" v-if="isLoading">
					<view class="loading-icon"></view>
					<text>正在思考中...</text>
				</view>
			</scroll-view>

			<!-- 输入区域 -->
			<view class="input-area">
				<input type="text" v-model="message" placeholder="请输入您的问题" @confirm="sendMessage"
					:disabled="isLoading" />
				<button @click="sendMessage" :disabled="isLoading">发送</button>
			</view>
		</view>
	</view>
</template>

<<script>
import {
    uniBadge,
    uniIcons
} from '@dcloudio/uni-ui'

export default {
    components: {
        uniBadge,
        uniIcons
    },
    data() {
        return {
            message: '',
            messages: [],
            isLoading: false,
            scrollTop: 0,
            isAIMode: false,
            scrollAnimation: true,
            qaPairs: {
                'Hello': 'Hello! Can i help you？',
                'I am very thirsty': 'Oh, if you are very thirsty, we would recommend you our fruit tea series.',
                'Thirsty': 'Oh, if you are very thirsty, we would recommend you our fruit tea series.',
                'Sleepy': 'For sleepy customers, Americano would be a good choice.',
                'Hot': 'Yes, the weather has been quite hot recently, you will definitely love the Rena Ice series',
                'Today is hot': 'Yes, the weather has been quite hot recently, you will definitely love the Rena Ice series',
                'Time': 'You can order drinks between 9:00-22:00. Hope you have a nice day',
                'Discount': 'New users can receive coupons when they register. Please check the event page for specific discounts.',
                'Pay': 'Supports multiple payment methods such as WeChat Pay and Alipay.',
                'Order': 'You can check the status of your order in "My Shopcart".',
                'VIP': 'Becoming a member can enjoy more benefits. Please check the member center for specific rights and interests.',
                'How are you': 'I am fine thank you , what can i help you?',
                'Cold': 'If the weather is cold, the hot latte series will be more popular.',
				'你好': '你好，很高兴为你服务，请问有什么能够帮到你？',
				'热': '是的，最近天气比较炎热，我推荐您试一下瑞纳冰系列产品，非常冰爽可口哦！',
				'口渴': '如果是想解渴的话，水果茶系列产品将是最好的选择！',
				'困': '美式咖啡会是提神利器，下单试试看吧.',
				'冷': '如果感觉寒冷的话,一些热拿铁系列会比较适合.',
            } 
        }
    },
    created() {
        this.loadChatHistory();
    },
    methods: {
        scrollToBottom() {
            const query = uni.createSelectorQuery().in(this);
            query.select('.message-list').boundingClientRect(data => {
                if (data) {
                    this.scrollAnimation = true;
                    this.scrollTop = data.height + 1000;
                }
            }).exec();
        },
        showClearConfirm() {
            uni.showModal({
                title: '提示',
                content: '确定要清空聊天记录吗？',
                success: (res) => {
                    if (res.confirm) {
                        this.clearChatHistory();
                    }
                }
            });
        },
        loadChatHistory() {
            try {
                const history = uni.getStorageSync('chatHistory');
                if (history) {
                    this.messages = JSON.parse(history);
                    this.$nextTick(() => {
                        this.scrollTop = 999999;
                    });
                }
            } catch (e) {
                console.error('加载历史对话失败:', e);
            }
        },
        saveChatHistory() {
            try {
                const recentMessages = this.messages.slice(-50);
                uni.setStorageSync('chatHistory', JSON.stringify(recentMessages));
            } catch (e) {
                console.error('保存对话历史失败:', e);
            }
        },
        clearChatHistory() {
            try {
                uni.removeStorageSync('chatHistory');
                this.messages = [];
                this.messages.push({
                    role: 'assistant',
                    content: this.isAIMode ?
                        'The conversation history has been cleared. Free for asking me' :
                        'The conversation history has been cleared. Ask me question again'
                });
            } catch (e) {
                console.error('清空对话历史失败:', e);
            }
        },
        toggleMode() {
            this.isAIMode = !this.isAIMode;
            const message = {
                role: 'assistant',
                content: this.isAIMode ?
                    'AI customer service mode and can answer your more complex questions.' :
                    'Quick customer service mode. I can quickly answer some of your simple questions.'
            };
            this.messages.push(message);
            this.saveChatHistory();
            this.$nextTick(() => {
                this.scrollToBottom();
            });
        },
        async sendMessage() {
            if (!this.message.trim() || this.isLoading) return;

            console.log('Send message:', this.message);
            const userMessage = {
                role: 'user',
                content: this.message
            };
            this.messages.push(userMessage);
            this.message = '';
            this.saveChatHistory();

            this.scrollToBottom();
            if (this.isAIMode) {
                await this.getAIResponse();
            } else {
                this.getQuickResponse();
            }
            this.saveChatHistory();
            this.$nextTick(() => {
                this.scrollTop = 999999;
            });
        },
        async getAIResponse() {
            this.isLoading = true;
            try {
                console.log('开始调用接口...');
                const response = await this.callLLMAPI(this.messages);
                console.log('Answer is :', response);
                if (response) {
                    this.messages.push({
                        role: 'assistant',
                        content: response
                    });
                    this.$nextTick(() => {
                        this.scrollToBottom();
                    });
                }
            } catch (error) {
                console.error('AI回复失败:', error);
                this.messages.push({
                    role: 'assistant',
                    content: 'Sorry, AI service is temporarily unavailable. Please try again later or switch to quick customer service mode.'
                });
                this.$nextTick(() => {
                    this.scrollToBottom();
                });
            } finally {
                this.isLoading = false;
            }
        },
        getQuickResponse() {
            const reply = this.getReply(this.messages[this.messages.length - 1].content);
            this.messages.push({
                role: 'assistant',
                content: reply
            });
            this.$nextTick(() => {
                this.scrollToBottom();
            });
        },
        getReply(message) {
            const lowerMessage = message.toLowerCase();
            for (const [key, value] of Object.entries(this.qaPairs)) {
                if (lowerMessage.includes(key.toLowerCase())) {
                    return value;
                }
            }
            return 'Sorry, I can not answer this question for now. You can try asking questions about: Time, Discount, Pay, Order, Vip, Recommend, etc.';
        },
        async callLLMAPI(messages) {
            try {
                const lastUserMessage = messages[messages.length - 1].content;
                
                return new Promise((resolve, reject) => {
                    uni.request({
                        url: 'http://127.0.0.1:8000/chat_enhanced',
                        method: 'POST',
                        header: {
                            'Content-Type': 'application/json'
                        },
                        data: {
                            question: lastUserMessage
                        },
                        success: (res) => {
                            console.log('完整的API响应:', res);
                            console.log('响应数据:', res.data);
                            
                            if (res.statusCode === 200 && res.data && res.data.answer) {
                                resolve(res.data.answer);
                            } else {
                                console.error('响应格式不正确:', res);
                                reject(new Error('响应格式不正确'));
                            }
                        },
                        fail: (err) => {
                            console.error('请求失败:', err);
                            reject(err);
                        }
                    });
                });
            } catch (error) {
                console.error('API调用失败:', error);
                throw new Error('API调用失败');
            }
        },
        back() {
            uni.navigateBack({
                delta: 1
            });
        }
    }
}
</script>

<style lang="less" scoped>
	.customer-service {
		height: 100vh;
		background-color: #f7f7f7;
		position: relative;

		.background-image {
			position: fixed;
			top: 0;
			left: 0;
			right: 0;
			bottom: 0;
			background-image: url('/static/images/rxkf.png');
			background-size: 40px;
			background-position: center;
			filter: blur(px);
			opacity: 0.2;
			z-index: 0;
			background-repeat: no-repeat;
		}
		
		.loading {
			display: flex;
			align-items: center;
			justify-content: center;
			padding: 20rpx;

			.loading-icon {
				width: 40rpx;
				height: 40rpx;
				border: 4rpx solid #f3f3f3;
				border-top: 4rpx solid #0c34ba;
				border-radius: 50%;
				animation: spin 1s linear infinite;
				margin-right: 20rpx;
			}

			text {
				color: #999;
				font-size: 24rpx;
			}
		}

		.nav {
			height: 100rpx;
			padding: 0 30rpx;
			background-color: #fff;
			display: flex;
			align-items: center;
			justify-content: space-between;

			.nav-right {
				display: flex;
				align-items: center;
				gap: 20rpx;

				.clear-btn {
					padding: 10rpx;

					.icon-delete {
						font-size: 36rpx;
						color: #666;
					}

					&:active {
						opacity: 0.7;
					}
				}
			}

			.nav-left {
				display: flex;
				align-items: center;

				.back-text {
					color: #0c34ba;
					font-size: 28rpx;
					margin-left: 10rpx;
				}
			}

			.title {
				font-size: 32rpx;
				font-weight: bold;
				color: #333;
			}

			.mode-switch {
				padding: 10rpx 20rpx;
				background-color: #0c34ba;
				color: #fff;
				border-radius: 30rpx;
				font-size: 24rpx;

				&:active {
					opacity: 0.8;
				}
			}
		}

		.chat-area {
			height: calc(100vh - 100rpx);
			display: flex;
			flex-direction: column;
			position: relative; // 添加相对定位

			.message-list {

				flex: 1;
				padding: 20rpx 30rpx;
				padding-bottom: 120rpx; // 为底部输入框留出空间
				overflow-y: auto; // 允许内容滚动
				-webkit-overflow-scrolling: touch; // 增加 iOS 滚动惯性

				.message-item {
					margin-bottom: 20rpx;
					display: flex;

					.message-content {
						max-width: 70%;
						padding: 20rpx;
						border-radius: 20rpx;
						font-size: 28rpx;
						line-height: 1.5;
					}

					&.user-message {
						justify-content: flex-end;
						padding-left: 30rpx; // 左侧留出空间

						.message-content {
							margin-right: 50rpx; // 增加右侧外边距
							background-color: #0c34ba;
							color: #fff;
						}
					}

					&.bot-message {
						justify-content: flex-start;
						padding-right: 30rpx; // 右侧留出空间

						.message-content {
							margin-left: 30rpx; // 增加左侧外边距
							background-color: #fff;
							color: #333;
						}
					}
				}
			}

			.input-area {
				position: fixed; // 改为固定定位
				bottom: 0; // 固定在底部
				left: 0;
				right: 0;
				padding: 20rpx;
				background-color: #fff;
				border-top: 1rpx solid #eee;
				display: flex;
				align-items: center;
				z-index: 99; // 确保在最上层

				input {
					flex: 1;
					height: 80rpx;
					padding: 0 20rpx;
					background-color: #f7f7f7;
					border-radius: 40rpx;
					margin-right: 20rpx;
				}

				button {
					width: 160rpx;
					height: 80rpx;
					line-height: 80rpx;
					background-color: #0c34ba;
					color: #fff;
					border-radius: 40rpx;
					font-size: 28rpx;

					&[disabled] {
						opacity: 0.5;
					}
				}
			}
		}
	}

	@keyframes spin {
		0% {
			transform: rotate(0deg);
		}

		100% {
			transform: rotate(360deg);
		}
	}
</style>