<template>
    <view>
        <view class="shopping">
            <view class="shopping-nav">
                购物车
            </view>
            
            <!-- 购物车为空时显示 -->
            <view class="shopping-container" v-if="!cartItems.length">
                <view class="shopping-icon">
                    <image class="icon-picture" src="../../static/shopping-icon.png"></image>
                </view>
                <view class="shopping-des">
                    空空如也
                </view>
                <view class="shopping-btns" @click="gotoMenu()">
                    添加商品
                </view>
            </view>

            <!-- 购物车有商品时显示 -->
            <view class="cart-list" v-else>
                <!-- 全选按钮 -->
                <view class="select-all">
                    <checkbox-group @change="selectAll">
                        <label class="checkbox">
                            <checkbox :checked="isAllSelected" color="#0c34ba"/>
                            <text>全选</text>
                        </label>
                    </checkbox-group>
                    <text class="delete-btn" @click="deleteSelected">删除选中</text>
                </view>

                <view class="cart-item" v-for="(item, index) in cartItems" :key="index">
                    <checkbox-group @change="selectItem($event, index)">
                        <label class="checkbox">
                            <checkbox :checked="item.selected" color="#0c34ba"/>
                        </label>
                    </checkbox-group>
                    <image class="item-img" :src="item.large_img" mode="aspectFill"></image>
                    <view class="item-info">
                        <view class="item-name">{{item.name}}</view>
                        <view class="item-specs">
                            <text v-for="(spec, i) in item.specs" :key="i">
                                {{spec.name}}: {{spec.value}}
                            </text>
                        </view>
                        <view class="item-price">
                            <text class="price">￥{{item.price}}</text>
                            <view class="item-count">
                                <text class="count-btn" @click="changeCount(index, -1)">-</text>
                                <text class="count-num">{{item.num}}</text>
                                <text class="count-btn" @click="changeCount(index, 1)">+</text>
                            </view>
                        </view>
                    </view>
                </view>

                <!-- 底部结算栏 -->
                <view class="settlement-bar">
                    <view class="settlement-left">
                        <checkbox-group @change="selectAll">
                            <label class="checkbox">
                                <checkbox :checked="isAllSelected" color="#0c34ba"/>
                                <text>全选</text>
                            </label>
                        </checkbox-group>
                        <view class="total-info">
                            <text>合计：</text>
                            <text class="total-price">￥{{selectedTotalPrice}}</text>
                        </view>
                    </view>
                    <view class="settlement-right" @click="handlePayment">
                        立即付款
                    </view>
                </view>
            </view>
        </view>
    </view>
</template>

<script>
export default {
    data() {
        return {
            isLogin: false,
            cartItems: [],
            totalPrice: 0,
            isAllSelected: false,
            selectedTotalPrice: '0.00'
        }
    },
    
    onShow() {
        this.checkLogin();
        this.loadCartItems();
    },
    
    methods: {
        checkLogin() {
            try {
                const tokenStr = localStorage.getItem("token");
                if (!tokenStr) {
                    this.isLogin = false;
                    this.showLoginToast();
                    return;
                }

                const token = JSON.parse(tokenStr);
                this.isLogin = !!token;
                
                if (!this.isLogin) {
                    this.showLoginToast();
                }
            } catch (error) {
                console.error('Token解析错误:', error);
                this.isLogin = false;
                this.showLoginToast();
            }
        },

        showLoginToast() {
            uni.showToast({
                title: "您未登录过",
                icon: 'none'
            });
            
            setTimeout(() => {
                uni.navigateTo({
                    url: "/pages/login/login"
                });
            }, 1000);
        },

        loadCartItems() {
            try {
                const itemsStr = uni.getStorageSync('cartItems');
                if (!itemsStr) {
                    this.cartItems = [];
                    return;
                }

                const items = JSON.parse(itemsStr);
                this.cartItems = Array.isArray(items) ? items.map(item => ({
                    ...item,
                    selected: item.selected || false
                })) : [];
                
                this.calculateTotal();
                this.calculateSelectedTotal();
                this.isAllSelected = this.cartItems.length > 0 && this.cartItems.every(item => item.selected);
            } catch (error) {
                console.error('购物车数据加载错误:', error);
                this.cartItems = [];
            }
        },

        calculateTotal() {
            try {
                this.totalPrice = this.cartItems.reduce((total, item) => {
                    const price = parseFloat(item.price) || 0;
                    const num = parseInt(item.num) || 0;
                    return total + (price * num);
                }, 0).toFixed(2);
            } catch (error) {
                console.error('计算总价错误:', error);
                this.totalPrice = '0.00';
            }
        },

        calculateSelectedTotal() {
            try {
                const selectedItems = this.cartItems.filter(item => item.selected);
                this.selectedTotalPrice = selectedItems.reduce((total, item) => {
                    const price = parseFloat(item.price) || 0;
                    const num = parseInt(item.num) || 0;
                    return total + (price * num);
                }, 0).toFixed(2);
            } catch (error) {
                console.error('计算选中商品总价错误:', error);
                this.selectedTotalPrice = '0.00';
            }
        },

        changeCount(index, change) {
            try {
                const item = this.cartItems[index];
                if (!item) return;

                if (item.num + change <= 0) {
                    uni.showModal({
                        title: '提示',
                        content: '是否删除该商品？',
                        success: (res) => {
                            if (res.confirm) {
                                this.cartItems.splice(index, 1);
                                this.saveCartItems();
                                this.calculateSelectedTotal();
                            }
                        }
                    });
                    return;
                }

                item.num += change;
                this.saveCartItems();
                this.calculateSelectedTotal();
            } catch (error) {
                console.error('修改数量错误:', error);
                uni.showToast({
                    title: '操作失败',
                    icon: 'none'
                });
            }
        },

        saveCartItems() {
            try {
                uni.setStorageSync('cartItems', JSON.stringify(this.cartItems));
                this.calculateTotal();
                this.calculateSelectedTotal();
            } catch (error) {
                console.error('保存购物车数据错误:', error);
                uni.showToast({
                    title: '保存失败',
                    icon: 'none'
                });
            }
        },

        gotoMenu() {
            uni.showToast({
                title: "正在加载中",
                icon: 'none'
            });
            
            setTimeout(() => {
                uni.switchTab({
                    url: "/pages/menu/menu"
                });
            }, 500);
        },

        selectAll(e) {
            const checked = e.detail.value.length > 0;
            this.isAllSelected = checked;
            this.cartItems.forEach(item => {
                item.selected = checked;
            });
            this.saveCartItems();
            this.calculateSelectedTotal();
        },

        selectItem(e, index) {
            const checked = e.detail.value.length > 0;
            this.cartItems[index].selected = checked;
            this.isAllSelected = this.cartItems.every(item => item.selected);
            this.saveCartItems();
            this.calculateSelectedTotal();
        },

        deleteSelected() {
            if (!this.cartItems.some(item => item.selected)) {
                uni.showToast({
                    title: '请选择要删除的商品',
                    icon: 'none'
                });
                return;
            }

            uni.showModal({
                title: '提示',
                content: '确定要删除选中的商品吗？',
                success: (res) => {
                    if (res.confirm) {
                        this.cartItems = this.cartItems.filter(item => !item.selected);
                        this.saveCartItems();
                        uni.showToast({
                            title: '删除成功',
                            icon: 'success'
                        });
                    }
                }
            });
        },

        handlePayment() {
            const selectedItems = this.cartItems.filter(item => item.selected);
            if (selectedItems.length === 0) {
                uni.showToast({
                    title: '请选择要购买的商品',
                    icon: 'none'
                });
                return;
            }

            uni.showToast({
                title: '功能开发中，敬请期待',
                icon: 'none',
                duration: 2000
            });
        }
    }
}
</script>

<style>
.shopping {
    height: 100vh;
    background-color: #efeff0;
    font-family: "黑体";
    padding-bottom: 120rpx; /* 为底部结算栏留出空间 */
}

.shopping-nav {
     display: flex;
     justify-content: center;
     align-items: center;
     height: 100rpx;
     background-color: #0c34ba;
     color: #fff;
     letter-spacing: 2.55px;
     font-size: 20px;
     position: fixed;
     top: 0;
     left: 0;
     right: 0;
     z-index: 100;
}

.shopping-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    font-size: 48rpx;
    padding-top: 100rpx; /* 为导航栏留出空间 */
}

.shopping-icon {
    width: 180rpx;
    height: 180rpx;
    padding: 50rpx;
    border-radius: 50%;
    overflow: hidden;
    background-color: #e5e5e5;
}

.icon-picture {
    width: 100%;
    height: 100%;
    display: block;
}

.shopping-des {
    padding: 70rpx 0;
    font-size: 20px;
}

.shopping-btns {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 45%;
    height: 80rpx;
    background-color: #0c34ba;
    border-radius: 60rpx;
    color: #fff;
    letter-spacing: 1px;
    font-size: 18px;
}

.cart-list {
    padding: 20rpx;
    padding-top: 120rpx; /* 为导航栏留出空间 */
    padding-bottom: 150rpx; /* 为底部结算栏留出空间 */
}

.select-all {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20rpx;
    background-color: #fff;
    margin-bottom: 20rpx;
    border-radius: 10rpx;
}

.checkbox {
    display: flex;
    align-items: center;
}

.checkbox text {
    margin-left: 10rpx;
}

.delete-btn {
    color: #ff4d4f;
    font-size: 28rpx;
}

.cart-item {
    display: flex;
    align-items: center;
    background-color: #fff;
    padding: 20rpx;
    margin-bottom: 20rpx;
    border-radius: 10rpx;
}

.cart-item .checkbox {
    margin-right: 20rpx;
}

.item-img {
    width: 160rpx;
    height: 160rpx;
    border-radius: 10rpx;
}

.item-info {
    flex: 1;
    margin-left: 20rpx;
}

.item-name {
    font-size: 32rpx;
    font-weight: bold;
    margin-bottom: 10rpx;
}

.item-specs {
    font-size: 24rpx;
    color: #666;
    margin-bottom: 10rpx;
}

.item-specs text {
    margin-right: 20rpx;
}

.item-price {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.price {
    color: #0c34ba;
    font-size: 32rpx;
    font-weight: bold;
}

.item-count {
    display: flex;
    align-items: center;
}

.count-btn {
    width: 50rpx;
    height: 50rpx;
    line-height: 50rpx;
    text-align: center;
    background-color: #f5f5f5;
    border-radius: 25rpx;
}

.count-num {
    margin: 0 20rpx;
}

/* 底部结算栏样式 */
.settlement-bar {
    position: fixed;
    bottom: var(--window-bottom, 0);  /* 适配底部安全区域 */
    left: 0;
    right: 0;
    height: 100rpx;
    background-color: #fff;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 30rpx;
    box-shadow: 0 -2rpx 10rpx rgba(0,0,0,0.1);
    z-index: 999;  /* 提高层级 */
}

.settlement-left {
    display: flex;
    align-items: center;
    flex: 1;  /* 添加弹性布局 */
}

.total-info {
    margin-left: 20rpx;
    flex: 1;  /* 添加弹性布局 */
}

.total-price {
    color: #0c34ba;
    font-size: 32rpx;
    font-weight: bold;
}

.settlement-right {
    background-color: #0c34ba;
    color: #fff;
    padding: 20rpx 40rpx;  /* 调整padding */
    border-radius: 40rpx;
    font-size: 28rpx;
    margin-left: 20rpx;  /* 添加左边距 */
}
</style>