let ajaxNumber = 0;
const request = obj => {
	ajaxNumber++;
	const baseUrl = "http://newcoffee.wwp666.cn:10006";
	return new Promise((resolve,reject) => {
		// uni.showLoading({
		// 	title:"加载中"
		// })
		uni.request({
			...obj,
			url: baseUrl + obj.url,
			data:{
				appkey:"U2FsdGVkX19WSQ59Cg+Fj9jNZPxRC5y0xB1iV06BeNA=",
				...obj.data
			},
			success:(res) => {
				resolve(res.data.result);
				
				ajaxNumber--;
				
				if(ajaxNumber == 0){
					setTimeout(() => {
						uni.hideLoading();
					},1000)
					
				}
				// console.log(99);
			}
		})
	}
	)
}

export default{
	request
}