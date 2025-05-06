<template>
	<view class="customer-service">
		<!-- 背景图片 -->
		<view class="background-image"></view>

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
			<text class="title">校园客服</text>
			<view class="nav-right">
				<!-- 添加语音按钮 -->
				<view class="voice-btn" @click="toggleVoiceInput">
					<text class="icon-voice">{{ isListening ? '🎤' : '🎤' }}</text>
				</view>
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
				<view class="voice-recording" v-if="isListening">
					<view class="recording-icon"></view>
					<text>正在聆听...</text>
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

<script>
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
				isListening: false,
				recognition: null,
				qaPairs: {
					'Hello': 'Hello! Can i help you？',
					'I am very hungry': 'Oh, if you are very hungry, u can go to the canteen to eat something.',
					'Hungry': 'Oh, if you are very hungry, u can go to the canteen to eat something.',
					'Sleepy': 'For sleepy students, take a cup of Americano would be a good choice.',
					'Hot': 'Yes, the weather has been quite hot recently, what about swimming in the pool?',
					'Today is hot': 'Yes, the weather has been quite hot recently, what about swimming in the pool?',
					'Time': 'You can order drinks between 9:00-22:00. Hope you have a nice day',
					'Discount': 'If u are HSUHK students u can enjoy it. Please check the event page for specific discounts.',
					'Pay': 'Supports multiple payment methods such as WeChat Pay and Alipay.',
					'Library': 'You can use library at 8am to 10pm.',
					'Gym': 'You can use gym at 9am to 8pm. Please check the member center for specific rights and interests.',
					'How are you': 'I am fine thank you , what can i help you?',
					'Bus': 'You can take bus after H building.',
					'你好': '你好，很高兴为你服务，请问有什么能够帮到你？',
					'热': '是的，最近天气比较炎热，可以去体育馆游泳哦！',
					'口渴': '如果是想解渴的话，食堂有港式饮品，学校也布置了多台饮料贩卖机！',
					'困': '美式咖啡会是提神利器，在利楼楼下试试看吧.',
					'巴士': '大佬山隧道有很多巴士可以乘坐.',
				}
			}
		},
		created() {
			this.loadChatHistory();
			this.initSpeechRecognition();
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
			initSpeechRecognition() {
				if ('webkitSpeechRecognition' in window) {
					this.recognition = new webkitSpeechRecognition();
					this.recognition.continuous = false;
					this.recognition.interimResults = false;
					this.recognition.lang = 'zh-CN';

					this.recognition.onresult = (event) => {
						const transcript = event.results[0][0].transcript;
						this.message = transcript;
						this.sendMessage();
					};

					this.recognition.onerror = (event) => {
						console.error('语音识别错误:', event.error);
						this.isListening = false;
					};

					this.recognition.onend = () => {
						this.isListening = false;
					};
				} else {
					uni.showToast({
						title: '您的浏览器不支持语音识别',
						icon: 'none'
					});
				}
			},
			toggleVoiceInput() {
				if (!this.recognition) {
					uni.showToast({
						title: '语音识别不可用',
						icon: 'none'
					});
					return;
				}

				if (this.isListening) {
					this.recognition.stop();
				} else {
					this.recognition.start();
					this.isListening = true;
				}
			},
			speakText(text) {
				// 使用Web Speech API进行语音合成
				if ('speechSynthesis' in window) {
					const utterance = new SpeechSynthesisUtterance(text);
					utterance.lang = 'zh-CN';
					utterance.rate = 1.0;
					utterance.volume = 1.0;

					// 设置中文语音
					const voices = speechSynthesis.getVoices();
					const chineseVoice = voices.find(voice => voice.lang.includes('zh'));
					if (chineseVoice) {
						utterance.voice = chineseVoice;
					}

					speechSynthesis.speak(utterance);

					// 监听语音播放完成事件
					utterance.onend = () => {
						console.log('语音播放完成');
					};

					// 监听语音播放错误事件
					utterance.onerror = (event) => {
						console.error('语音播放失败:', event);
						uni.showToast({
							title: '语音播放失败',
							icon: 'none'
						});
					};
				} else {
					uni.showToast({
						title: '当前浏览器不支持语音播放',
						icon: 'none'
					});
				}
				// 使用uni-app的语音合成API
				/*	uni.showToast({
						title: '正在播放语音...',
						icon: 'none'
					});

					// 创建语音合成实例
					const TTSManager = uni.createInnerAudioContext();
					TTSManager.src = `https://tts.baidu.com/text2audio?lan=zh&ie=UTF-8&text=${encodeURIComponent(text)}`;
					TTSManager.play();

					TTSManager.onPlay(() => {
						console.log('开始播放语音');
					});

					TTSManager.onError((res) => {
						console.error('语音播放失败:', res);
						uni.showToast({
							title: '语音播放失败',
							icon: 'none'
						});
					});*/
			},
			async sendMessage() {
				if (!this.message.trim() || this.isLoading) return;

				const userMessage = {
					role: 'user',
					content: this.message
				};
				this.messages.push(userMessage);
				this.message = '';
				this.saveChatHistory();

				this.scrollToBottom();
				let response;
				if (this.isAIMode) {
					//await this.getAIResponse();
					response = await this.getAIResponse();
				} else {
					//this.getQuickResponse();
					response = this.getQuickResponse();
				}
				if (response) {
					// 延迟一下再播放语音，让用户有时间看到文字回复
					setTimeout(() => {
						this.speakText(response);
					}, 500);
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
							url: 'http://127.0.0.1:8000/chat',
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
			background-image: url('/static/images/hsu.png');
			background-size: px;
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
			position: relative;
			z-index: 1;

			.loading-icon {
				width: 40rpx;
				height: 40rpx;
				border: 4rpx solid #f3f3f3;
				border-top: 4rpx solid #2E7D32;
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
			position: relative;
			z-index: 1;

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

				.voice-btn {
					padding: 10rpx;
					margin-right: 10rpx;

					.icon-voice {
						font-size: 36rpx;
						color: #2E7D32;
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
					color: #2E7D32;
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
				background-color: #2E7D32;
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
			position: relative;
			z-index: 1;

			.message-list {
				flex: 1;
				padding: 20rpx 30rpx;
				padding-bottom: 120rpx;
				overflow-y: auto;
				-webkit-overflow-scrolling: touch;

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
						padding-left: 30rpx;

						.message-content {
							margin-right: 50rpx;
							background-color: #2E7D32;
							color: #fff;
						}
					}

					&.bot-message {
						justify-content: flex-start;
						padding-right: 30rpx;

						.message-content {
							margin-left: 30rpx;
							background-color: #fff;
							color: #333;
						}
					}
				}
			}

			.input-area {
				position: fixed;
				bottom: 0;
				left: 0;
				right: 0;
				padding: 20rpx;
				background-color: #fff;
				border-top: 1rpx solid #eee;
				display: flex;
				align-items: center;
				z-index: 99;

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
					background-color: #2E7D32;
					color: #fff;
					border-radius: 40rpx;
					font-size: 28rpx;

					&[disabled] {
						opacity: 0.5;
					}
				}
			}
		}

		.voice-recording {
			display: flex;
			align-items: center;
			justify-content: center;
			padding: 20rpx;
			position: relative;
			z-index: 1;

			.recording-icon {
				width: 20rpx;
				height: 20rpx;
				background-color: #2E7D32;
				border-radius: 50%;
				margin-right: 20rpx;
				animation: pulse 1.5s infinite;
			}

			text {
				color: #2E7D32;
				font-size: 24rpx;
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

	@keyframes pulse {
		0% {
			transform: scale(0.95);
			opacity: 0.5;
		}

		50% {
			transform: scale(1.2);
			opacity: 1;
		}

		100% {
			transform: scale(0.95);
			opacity: 0.5;
		}
	}
</style>