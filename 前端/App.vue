<script>
	export default {
		onLaunch: function() {
			console.log('App Launch')
		},
		onShow: function() {
			console.log('App Show')
		},
		onHide: function() {
			console.log('App Hide')
		}
	}
</script>

<style>
	/*每个页面公共css */
	/* 确保页面高度100% */
	page {
		height: 100%;
	}
	/* 防止导航栏遮挡内容 */
	.uni-tabbar-bottom {
		position: fixed;
		z-index: 999;
	}
	/* 调整中间按钮的图标大小 */
	.uni-tabbar__icon + .uni-tabbar__label {
		font-size: 24rpx;
	}
	/* 突出显示中间按钮 */
	.uni-tabbar__item:nth-child(3) .uni-tabbar__icon {
		width: 50rpx;
		height: 50rpx;
		margin-top: -20rpx;
	}
</style>
