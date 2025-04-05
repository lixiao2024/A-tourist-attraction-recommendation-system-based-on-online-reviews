(global["webpackJsonp"] = global["webpackJsonp"] || []).push([["pages/mine/mine"],{

/***/ 72:
/*!**************************************************************************!*\
  !*** I:/基于在线评论的旅游景点智能推荐系统/小程序/前端/main.js?{"page":"pages%2Fmine%2Fmine"} ***!
  \**************************************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";
/* WEBPACK VAR INJECTION */(function(wx, createPage) {

var _interopRequireDefault = __webpack_require__(/*! @babel/runtime/helpers/interopRequireDefault */ 4);
__webpack_require__(/*! uni-pages */ 26);
__webpack_require__(/*! @dcloudio/vue-cli-plugin-uni/packages/uni-cloud/dist/index.js */ 27);
var _vue = _interopRequireDefault(__webpack_require__(/*! vue */ 25));
var _mine = _interopRequireDefault(__webpack_require__(/*! ./pages/mine/mine.vue */ 73));
// @ts-ignore
wx.__webpack_require_UNI_MP_PLUGIN__ = __webpack_require__;
createPage(_mine.default);
/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! ./node_modules/@dcloudio/uni-mp-weixin/dist/wx.js */ 1)["default"], __webpack_require__(/*! ./node_modules/@dcloudio/uni-mp-weixin/dist/index.js */ 2)["createPage"]))

/***/ }),

/***/ 73:
/*!*******************************************************!*\
  !*** I:/基于在线评论的旅游景点智能推荐系统/小程序/前端/pages/mine/mine.vue ***!
  \*******************************************************/
/*! no static exports found */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _mine_vue_vue_type_template_id_dcbcfe34___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./mine.vue?vue&type=template&id=dcbcfe34& */ 74);
/* harmony import */ var _mine_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./mine.vue?vue&type=script&lang=js& */ 76);
/* harmony reexport (unknown) */ for(var __WEBPACK_IMPORT_KEY__ in _mine_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__) if(["default"].indexOf(__WEBPACK_IMPORT_KEY__) < 0) (function(key) { __webpack_require__.d(__webpack_exports__, key, function() { return _mine_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__[key]; }) }(__WEBPACK_IMPORT_KEY__));
/* harmony import */ var _mine_vue_vue_type_style_index_0_lang_css___WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./mine.vue?vue&type=style&index=0&lang=css& */ 78);
/* harmony import */ var _HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_runtime_componentNormalizer_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/vue-cli-plugin-uni/packages/vue-loader/lib/runtime/componentNormalizer.js */ 44);

var renderjs





/* normalize component */

var component = Object(_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_runtime_componentNormalizer_js__WEBPACK_IMPORTED_MODULE_3__["default"])(
  _mine_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__["default"],
  _mine_vue_vue_type_template_id_dcbcfe34___WEBPACK_IMPORTED_MODULE_0__["render"],
  _mine_vue_vue_type_template_id_dcbcfe34___WEBPACK_IMPORTED_MODULE_0__["staticRenderFns"],
  false,
  null,
  null,
  null,
  false,
  _mine_vue_vue_type_template_id_dcbcfe34___WEBPACK_IMPORTED_MODULE_0__["components"],
  renderjs
)

component.options.__file = "pages/mine/mine.vue"
/* harmony default export */ __webpack_exports__["default"] = (component.exports);

/***/ }),

/***/ 74:
/*!**************************************************************************************!*\
  !*** I:/基于在线评论的旅游景点智能推荐系统/小程序/前端/pages/mine/mine.vue?vue&type=template&id=dcbcfe34& ***!
  \**************************************************************************************/
/*! exports provided: render, staticRenderFns, recyclableRender, components */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_loaders_templateLoader_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_17_0_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_template_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_uni_app_loader_page_meta_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_mine_vue_vue_type_template_id_dcbcfe34___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/vue-cli-plugin-uni/packages/vue-loader/lib/loaders/templateLoader.js??vue-loader-options!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/vue-cli-plugin-uni/packages/webpack-preprocess-loader??ref--17-0!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/webpack-uni-mp-loader/lib/template.js!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/vue-cli-plugin-uni/packages/webpack-uni-app-loader/page-meta.js!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/vue-cli-plugin-uni/packages/vue-loader/lib??vue-loader-options!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/webpack-uni-mp-loader/lib/style.js!./mine.vue?vue&type=template&id=dcbcfe34& */ 75);
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "render", function() { return _HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_loaders_templateLoader_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_17_0_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_template_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_uni_app_loader_page_meta_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_mine_vue_vue_type_template_id_dcbcfe34___WEBPACK_IMPORTED_MODULE_0__["render"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "staticRenderFns", function() { return _HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_loaders_templateLoader_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_17_0_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_template_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_uni_app_loader_page_meta_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_mine_vue_vue_type_template_id_dcbcfe34___WEBPACK_IMPORTED_MODULE_0__["staticRenderFns"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "recyclableRender", function() { return _HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_loaders_templateLoader_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_17_0_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_template_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_uni_app_loader_page_meta_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_mine_vue_vue_type_template_id_dcbcfe34___WEBPACK_IMPORTED_MODULE_0__["recyclableRender"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "components", function() { return _HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_loaders_templateLoader_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_17_0_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_template_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_uni_app_loader_page_meta_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_mine_vue_vue_type_template_id_dcbcfe34___WEBPACK_IMPORTED_MODULE_0__["components"]; });



/***/ }),

/***/ 75:
/*!**************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/@dcloudio/vue-cli-plugin-uni/packages/vue-loader/lib/loaders/templateLoader.js??vue-loader-options!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/webpack-preprocess-loader??ref--17-0!./node_modules/@dcloudio/webpack-uni-mp-loader/lib/template.js!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/webpack-uni-app-loader/page-meta.js!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/vue-loader/lib??vue-loader-options!./node_modules/@dcloudio/webpack-uni-mp-loader/lib/style.js!I:/基于在线评论的旅游景点智能推荐系统/小程序/前端/pages/mine/mine.vue?vue&type=template&id=dcbcfe34& ***!
  \**************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************/
/*! exports provided: render, staticRenderFns, recyclableRender, components */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "render", function() { return render; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "staticRenderFns", function() { return staticRenderFns; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "recyclableRender", function() { return recyclableRender; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "components", function() { return components; });
var components
try {
  components = {
    uniIcons: function () {
<<<<<<< HEAD
      return Promise.all(/*! import() | uni_modules/uni-icons/components/uni-icons/uni-icons */[__webpack_require__.e("common/vendor"), __webpack_require__.e("uni_modules/uni-icons/components/uni-icons/uni-icons")]).then(__webpack_require__.bind(null, /*! @/uni_modules/uni-icons/components/uni-icons/uni-icons.vue */ 136))
=======
      return Promise.all(/*! import() | uni_modules/uni-icons/components/uni-icons/uni-icons */[__webpack_require__.e("common/vendor"), __webpack_require__.e("uni_modules/uni-icons/components/uni-icons/uni-icons")]).then(__webpack_require__.bind(null, /*! @/uni_modules/uni-icons/components/uni-icons/uni-icons.vue */ 141))
>>>>>>> 8586f270516785f262322293fab3e10846b71926
    },
  }
} catch (e) {
  if (
    e.message.indexOf("Cannot find module") !== -1 &&
    e.message.indexOf(".vue") !== -1
  ) {
    console.error(e.message)
    console.error("1. 排查组件名称拼写是否正确")
    console.error(
      "2. 排查组件是否符合 easycom 规范，文档：https://uniapp.dcloud.net.cn/collocation/pages?id=easycom"
    )
    console.error(
      "3. 若组件不符合 easycom 规范，需手动引入，并在 components 中注册该组件"
    )
  } else {
    throw e
  }
}
var render = function () {
  var _vm = this
  var _h = _vm.$createElement
  var _c = _vm._self._c || _h
  var l0 = _vm.__map(_vm.statsData, function (item, index) {
    var $orig = _vm.__get_orig(item)
    var m0 = _vm.getStatIcon(item.label)
    return {
      $orig: $orig,
      m0: m0,
    }
  })
  _vm.$mp.data = Object.assign(
    {},
    {
      $root: {
        l0: l0,
      },
    }
  )
}
var recyclableRender = false
var staticRenderFns = []
render._withStripped = true



/***/ }),

/***/ 76:
/*!********************************************************************************!*\
  !*** I:/基于在线评论的旅游景点智能推荐系统/小程序/前端/pages/mine/mine.vue?vue&type=script&lang=js& ***!
  \********************************************************************************/
/*! no static exports found */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _HBuilderX_plugins_uniapp_cli_node_modules_babel_loader_lib_index_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_13_1_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_script_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_mine_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/babel-loader/lib!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/vue-cli-plugin-uni/packages/webpack-preprocess-loader??ref--13-1!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/webpack-uni-mp-loader/lib/script.js!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/vue-cli-plugin-uni/packages/vue-loader/lib??vue-loader-options!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/webpack-uni-mp-loader/lib/style.js!./mine.vue?vue&type=script&lang=js& */ 77);
/* harmony import */ var _HBuilderX_plugins_uniapp_cli_node_modules_babel_loader_lib_index_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_13_1_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_script_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_mine_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_HBuilderX_plugins_uniapp_cli_node_modules_babel_loader_lib_index_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_13_1_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_script_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_mine_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__);
/* harmony reexport (unknown) */ for(var __WEBPACK_IMPORT_KEY__ in _HBuilderX_plugins_uniapp_cli_node_modules_babel_loader_lib_index_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_13_1_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_script_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_mine_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__) if(["default"].indexOf(__WEBPACK_IMPORT_KEY__) < 0) (function(key) { __webpack_require__.d(__webpack_exports__, key, function() { return _HBuilderX_plugins_uniapp_cli_node_modules_babel_loader_lib_index_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_13_1_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_script_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_mine_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__[key]; }) }(__WEBPACK_IMPORT_KEY__));
 /* harmony default export */ __webpack_exports__["default"] = (_HBuilderX_plugins_uniapp_cli_node_modules_babel_loader_lib_index_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_13_1_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_script_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_mine_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0___default.a); 

/***/ }),

/***/ 77:
/*!***************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/babel-loader/lib!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/webpack-preprocess-loader??ref--13-1!./node_modules/@dcloudio/webpack-uni-mp-loader/lib/script.js!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/vue-loader/lib??vue-loader-options!./node_modules/@dcloudio/webpack-uni-mp-loader/lib/style.js!I:/基于在线评论的旅游景点智能推荐系统/小程序/前端/pages/mine/mine.vue?vue&type=script&lang=js& ***!
  \***************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";
/* WEBPACK VAR INJECTION */(function(wx, uni) {

var _interopRequireDefault = __webpack_require__(/*! @babel/runtime/helpers/interopRequireDefault */ 4);
Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;
var _regenerator = _interopRequireDefault(__webpack_require__(/*! @babel/runtime/regenerator */ 28));
var _asyncToGenerator2 = _interopRequireDefault(__webpack_require__(/*! @babel/runtime/helpers/asyncToGenerator */ 31));
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
var _default = {
  data: function data() {
    return {
      isLogged: false,
      nickName: '',
      avatarUrl: '',
      showModal: false,
      canIUseGetUserProfile: false,
      // 是否支持getUserProfile
      statsData: [{
        label: '粉丝',
        value: 0,
        icon: 'person'
      }, {
        label: '获赞',
        value: 0,
        icon: 'heart'
      }, {
        label: '关注',
        value: 0,
        icon: 'eye'
      }, {
        label: '收藏',
        value: 45,
        icon: 'star'
      }],
      functionGroups: [[{
        label: '个人信息',
        type: 'info',
        icon: 'info'
      }, {
        label: '我的笔记',
        type: 'notes',
        icon: 'bars'
      }, {
        label: '我的足迹',
        type: 'footprint',
        icon: 'location'
      }, {
        label: '用户反馈',
        type: 'feedback',
        icon: 'chat'
      }]],
      loginStep: 1,
      tempAvatarUrl: '',
      tempNickName: ''
    };
  },
  onLoad: function onLoad() {
    console.log('页面加载，开始初始化...');
    // 检查是否支持getUserProfile
    if (wx.getUserProfile) {
      this.canIUseGetUserProfile = true;
      console.log('当前环境支持getUserProfile');
    } else {
      console.log('当前环境不支持getUserProfile，将使用getUserInfo');
    }

    // 直接刷新登录状态
    this.refreshLoginStatus();

    // 尝试从App全局状态获取登录信息
    var app = getApp();
    if (app.globalData && app.globalData.isLoggedIn && app.globalData.userInfo) {
      console.log('从App全局状态获取登录信息:', app.globalData.userInfo);
      this.avatarUrl = app.globalData.userInfo.avatar || app.globalData.userInfo.avatarUrl || '';
      this.nickName = app.globalData.userInfo.nickname || app.globalData.userInfo.nickName || '';
      this.isLogged = true;
    } else {
      // 检查登录状态并加载用户信息
      this.checkLoginStatus();
    }

    // 加载用户统计数据
    this.loadUserStatsData();

    // 添加全局登录成功事件监听
    uni.$on('loginSuccess', this.handleLoginSuccess);
    // 添加全局登录状态变化事件监听
    uni.$on('loginStatusChanged', this.handleLoginStatusChanged);
    console.log('页面初始化完成');
  },
  // 添加onShow生命周期，确保每次进入页面都检查登录状态
  onShow: function onShow() {
    console.log('页面显示，检查登录状态...');

    // 检查存储中的数据完整性
    this.checkStorageIntegrity();

    // 检查登录状态并加载用户信息
    this.checkLoginStatus();

    // 加载用户统计数据
    this.loadUserStatsData();
  },
  // 页面销毁时清除事件监听
  onUnload: function onUnload() {
    uni.$off('loginSuccess', this.handleLoginSuccess);
    uni.$off('loginStatusChanged', this.handleLoginStatusChanged);
  },
  methods: {
    // 检查存储数据的完整性，防止不一致
    checkStorageIntegrity: function checkStorageIntegrity() {
      console.log('检查存储数据完整性...');
      var token = uni.getStorageSync('token');
      var userInfo = uni.getStorageSync('userInfo');
      if (userInfo && !token) {
        // 有用户信息但没有token，创建临时token
        var tempToken = 'temp_' + new Date().getTime();
        uni.setStorageSync('token', tempToken);
        console.log('修复存储: 创建临时token', tempToken);
      }
      if (token && !userInfo) {
        // 有token但没有用户信息，尝试创建默认用户信息
        var defaultUserInfo = {
          nickname: '微信用户',
          avatar: '/static/default-avatar.png',
          nickName: '微信用户',
          avatarUrl: '/static/default-avatar.png'
        };
        uni.setStorageSync('userInfo', defaultUserInfo);
        console.log('修复存储: 创建默认用户信息');
      }

      // 如果有用户信息和token，检查全局状态是否同步
      if (token && userInfo) {
        var app = getApp();
        if (app && app.globalData && !app.globalData.isLoggedIn) {
          app.globalData.isLoggedIn = true;
          app.globalData.userInfo = userInfo;
          console.log('修复全局状态: 用户已登录但全局状态未同步');
        }
      }
    },
    // 显示登录模态框
    showLoginModal: function showLoginModal() {
      if (!this.isLogged) {
        this.showModal = true;
      } else {
        console.log('用户已登录，点击查看个人信息');
        // 可以跳转到个人信息页面
        uni.navigateTo({
          url: '/pages/mine/profile'
        });
      }
    },
    // 关闭登录模态框
    closeLoginModal: function closeLoginModal() {
      this.showModal = false;
      // 重置登录步骤
      this.loginStep = 1;
      this.tempNickName = '';
      this.tempAvatarUrl = '';
    },
    // 加载用户统计数据
    loadUserStatsData: function loadUserStatsData() {
      var _this = this;
      // 从本地存储获取用户统计数据
      var statsData = uni.getStorageSync('userStatsData');
      if (statsData && Array.isArray(statsData)) {
        // 更新页面上的统计数据
        statsData.forEach(function (item) {
          var index = _this.statsData.findIndex(function (stat) {
            return stat.label === item.label;
          });
          if (index !== -1) {
            _this.statsData[index].value = item.value;
          }
        });
      }
    },
    checkLoginStatus: function checkLoginStatus() {
      var _this2 = this;
      return (0, _asyncToGenerator2.default)( /*#__PURE__*/_regenerator.default.mark(function _callee() {
        var token, userInfo, app, _userInfo, tempToken;
        return _regenerator.default.wrap(function _callee$(_context) {
          while (1) {
            switch (_context.prev = _context.next) {
              case 0:
                _context.prev = 0;
                console.log('开始检查登录状态...');
                // 检查是否有token，判断用户是否已登录
                token = uni.getStorageSync('token');
                console.log('从存储中读取token:', token ? "\u5DF2\u83B7\u53D6: ".concat(token.substring(0, 10), "...") : '未获取');
                if (!token) {
                  _context.next = 22;
                  break;
                }
                userInfo = uni.getStorageSync('userInfo');
                console.log('从存储中读取用户信息:', userInfo ? JSON.stringify(userInfo).substring(0, 100) + '...' : '未获取');
                if (!userInfo) {
                  _context.next = 17;
                  break;
                }
                // 确保使用统一的属性名
                _this2.avatarUrl = userInfo.avatar || userInfo.avatarUrl || '';
                _this2.nickName = userInfo.nickname || userInfo.nickName || '';

                // 输出调试信息以便排查
                console.log('设置用户信息:', {
                  设置的头像: _this2.avatarUrl,
                  原始头像: userInfo.avatar || userInfo.avatarUrl,
                  设置的昵称: _this2.nickName,
                  原始昵称: userInfo.nickname || userInfo.nickName
                });
                _this2.isLogged = true;
                console.log('用户已登录，信息加载完成', _this2.nickName, _this2.avatarUrl);

                // 确保App全局状态也是最新的
                app = getApp();
                if (app && app.globalData) {
                  app.globalData.isLoggedIn = true;
                  app.globalData.userInfo = userInfo;
                  console.log('同步更新App全局状态');
                }
                _context.next = 20;
                break;
              case 17:
                // 有token但无用户信息时，尝试从后端获取用户信息
                console.log('有token但无用户信息，尝试获取用户数据');
                _context.next = 20;
                return _this2.fetchUserInfo(token);
              case 20:
                _context.next = 24;
                break;
              case 22:
                // 检查是否有其他登录依据（如userInfo）
                _userInfo = uni.getStorageSync('userInfo');
                if (_userInfo) {
                  console.log('虽然没有token，但找到了用户信息', _userInfo);
                  // 仍然使用用户信息更新界面
                  _this2.avatarUrl = _userInfo.avatar || _userInfo.avatarUrl || '';
                  _this2.nickName = _userInfo.nickname || _userInfo.nickName || '';
                  _this2.isLogged = true;
                  console.log('基于用户信息更新登录状态');

                  // 创建一个临时token，确保后续逻辑正常
                  tempToken = 'temp_' + new Date().getTime();
                  uni.setStorageSync('token', tempToken);
                  console.log('创建临时token:', tempToken);
                } else {
                  _this2.isLogged = false;
                  _this2.avatarUrl = '';
                  _this2.nickName = '';
                  console.log('用户未登录');
                }
              case 24:
                _context.next = 30;
                break;
              case 26:
                _context.prev = 26;
                _context.t0 = _context["catch"](0);
                console.error('获取登录状态失败:', _context.t0);
                _this2.isLogged = false;
              case 30:
              case "end":
                return _context.stop();
            }
          }
        }, _callee, null, [[0, 26]]);
      }))();
    },
    // 从后端获取用户信息
    fetchUserInfo: function fetchUserInfo(token) {
      var _this3 = this;
      return (0, _asyncToGenerator2.default)( /*#__PURE__*/_regenerator.default.mark(function _callee2() {
        var openid, userId, wxUserInfo, userInfo;
        return _regenerator.default.wrap(function _callee2$(_context2) {
          while (1) {
            switch (_context2.prev = _context2.next) {
              case 0:
                try {
                  // 模拟API请求获取用户信息
                  // 实际项目中应替换为真实接口调用
                  console.log('向后端发送获取用户信息请求...');
                  // 由于是示例，这里我们直接从本地存储获取用户基本信息
                  // 实际项目中应该使用以下代码发送请求
                  /*
                  const result = await uni.request({
                  	url: 'http://localhost:8000/api/user/info',
                  	method: 'GET',
                  	header: {
                  		'Authorization': `Bearer ${token}`,
                  		'content-type': 'application/json'
                  	}
                  });
                  
                  if (result.statusCode === 200) {
                  	const userInfo = result.data;
                  	// 保存用户信息
                  	uni.setStorageSync('userInfo', userInfo);
                  	
                  	// 更新页面数据
                  	this.avatarUrl = userInfo.avatar;
                  	this.nickName = userInfo.nickname;
                  	this.isLogged = true;
                  }
                  */

                  // 模拟获取，检查openid是否存在
                  openid = uni.getStorageSync('openid');
                  userId = uni.getStorageSync('user_id');
                  if (openid || userId) {
                    console.log('找到用户ID，尝试从其他信息重建用户数据');
                    // 尝试从本地存储中获取微信用户信息
                    wxUserInfo = uni.getStorageSync('wx_user_info');
                    if (wxUserInfo) {
                      // 如果存在微信用户信息，使用它
                      userInfo = {
                        nickname: wxUserInfo.nickName,
                        avatar: wxUserInfo.avatarUrl
                      };
                      console.log('使用存储的微信用户信息:', userInfo);
                    } else {
                      // 否则使用默认值
                      userInfo = {
                        nickname: '微信用户',
                        avatar: '/static/default-avatar.png'
                      };
                      console.log('使用默认用户信息，无法获取微信资料');
                    }

                    // 保存到本地
                    uni.setStorageSync('userInfo', userInfo);

                    // 更新页面数据
                    _this3.avatarUrl = userInfo.avatar;
                    _this3.nickName = userInfo.nickname;
                    _this3.isLogged = true;
                  }
                } catch (error) {
                  console.error('获取用户信息失败:', error);
                }
              case 1:
              case "end":
                return _context2.stop();
            }
          }
        }, _callee2);
      }))();
    },
    // 处理微信登录
    getUserProfile: function getUserProfile() {
      var _this4 = this;
      console.log('调用getUserProfile获取用户信息');
      uni.showLoading({
        title: '登录中...'
      });

      // 调用wx.getUserProfile获取用户信息
      wx.getUserProfile({
        desc: '用于完善会员资料',
        // 声明获取用户个人信息后的用途，会展示在弹窗中
        success: function success(res) {
          console.log('获取到用户个人信息:', res.userInfo);

          // 保存微信原始用户信息，以便后续使用
          uni.setStorageSync('wx_user_info', res.userInfo);

          // 预填充临时头像和昵称
          _this4.tempAvatarUrl = res.userInfo.avatarUrl;
          _this4.tempNickName = res.userInfo.nickName;

          // 如果获取到的是"微信用户"或默认头像，则进入完善信息步骤
          if (res.userInfo.nickName === '微信用户' || !res.userInfo.avatarUrl) {
            console.log('获取到默认昵称或头像，进入完善信息步骤');
            _this4.loginStep = 2;
            uni.hideLoading();
          } else {
            // 否则直接使用获取到的信息登录
            // 获取到用户信息后，继续获取微信code并调用后端API
            _this4.loginWithWechat(res.userInfo);
          }
        },
        fail: function fail(err) {
          console.error('用户拒绝授权:', err);
          uni.hideLoading();
          uni.showToast({
            title: '需要授权才能登录',
            icon: 'none'
          });
        }
      });
    },
    // 兼容旧版微信的获取用户信息方法
    getUserInfo: function getUserInfo(e) {
      console.log('通过getUserInfo获取用户信息');
      if (e.detail.userInfo) {
        // 用户同意授权
        console.log('获取到用户个人信息:', e.detail.userInfo);

        // 保存微信原始用户信息，以便后续使用
        uni.setStorageSync('wx_user_info', e.detail.userInfo);

        // 预填充临时头像和昵称
        this.tempAvatarUrl = e.detail.userInfo.avatarUrl;
        this.tempNickName = e.detail.userInfo.nickName;

        // 如果获取到的是"微信用户"或默认头像，则进入完善信息步骤
        if (e.detail.userInfo.nickName === '微信用户' || !e.detail.userInfo.avatarUrl) {
          console.log('获取到默认昵称或头像，进入完善信息步骤');
          this.loginStep = 2;
          uni.hideLoading();
        } else {
          // 否则直接使用获取到的信息登录
          this.loginWithWechat(e.detail.userInfo);
        }
      } else {
        // 用户拒绝授权
        console.error('用户拒绝授权');
        uni.showToast({
          title: '需要授权才能登录',
          icon: 'none'
        });
      }
    },
    // 使用微信登录
    loginWithWechat: function loginWithWechat(userInfo) {
      var _this5 = this;
      // 获取微信code
      uni.login({
        provider: 'weixin',
        success: function () {
          var _success = (0, _asyncToGenerator2.default)( /*#__PURE__*/_regenerator.default.mark(function _callee3(loginRes) {
            var localUserInfo, backendUrl, result, data, savedToken, _result$data;
            return _regenerator.default.wrap(function _callee3$(_context3) {
              while (1) {
                switch (_context3.prev = _context3.next) {
                  case 0:
                    _context3.prev = 0;
                    console.log('获取到微信登录code:', loginRes.code);

                    // 保存微信登录信息到本地，即使后端不可用也能显示头像和昵称
                    localUserInfo = {
                      nickname: userInfo.nickName,
                      avatar: userInfo.avatarUrl,
                      gender: userInfo.gender,
                      country: userInfo.country,
                      province: userInfo.province,
                      city: userInfo.city,
                      language: userInfo.language
                    };
                    uni.setStorageSync('userInfo', localUserInfo);

                    // 更新页面显示
                    _this5.nickName = userInfo.nickName;
                    _this5.avatarUrl = userInfo.avatarUrl;

                    // 调用后端API进行登录验证
                    console.log('准备向后端发送登录请求...');

                    // 使用实际IP地址替换localhost
                    // const backendUrl = 'http://localhost:8000/api/wechat-login';
                    backendUrl = 'http://192.168.1.10:8000/api/wechat-login'; // 替换为您的实际IP
                    _context3.prev = 8;
                    _context3.next = 11;
                    return uni.request({
                      url: backendUrl,
                      method: 'POST',
                      data: {
                        code: loginRes.code,
                        user_info: {
                          nickname: userInfo.nickName,
                          avatar_url: userInfo.avatarUrl,
                          gender: userInfo.gender,
                          country: userInfo.country,
                          province: userInfo.province,
                          city: userInfo.city,
                          language: userInfo.language
                        }
                      },
                      header: {
                        'content-type': 'application/json'
                      },
                      timeout: 10000 // 增加超时时间
                    });
                  case 11:
                    result = _context3.sent;
                    console.log('收到后端响应:', result);

                    // 检查请求是否成功
                    if (result.statusCode === 200) {
                      data = result.data;
                      console.log('登录成功, 获取到token和openid:', {
                        token: data.access_token,
                        openid: data.openid,
                        user_id: data.user_id
                      });

                      // 保存登录状态
                      uni.setStorageSync('token', data.access_token);
                      uni.setStorageSync('openid', data.openid);
                      uni.setStorageSync('user_id', data.user_id);

                      // 记录日志，确认token是否保存成功
                      savedToken = uni.getStorageSync('token');
                      console.log('保存并验证token成功:', savedToken ? '√ 已保存' : '× 未保存');

                      // 发布全局登录成功事件，通知其他页面更新状态
                      uni.$emit('loginSuccess', {
                        isLoggedIn: true,
                        userInfo: localUserInfo,
                        token: data.access_token // 显式包含token
                      });

                      // 标记为已登录
                      _this5.isLogged = true;
                      uni.showToast({
                        title: '登录成功'
                      });
                    } else {
                      console.error('登录失败:', result.data);
                      uni.showToast({
                        title: ((_result$data = result.data) === null || _result$data === void 0 ? void 0 : _result$data.detail) || '登录失败',
                        icon: 'none'
                      });

                      // 如果后端返回错误但我们已经保存了用户信息，仍然允许本地登录
                      _this5.isLogged = true;
                      uni.showToast({
                        title: '本地登录成功'
                      });
                    }
                    _context3.next = 21;
                    break;
                  case 16:
                    _context3.prev = 16;
                    _context3.t0 = _context3["catch"](8);
                    console.error('登录请求异常:', _context3.t0);

                    // 即使后端请求失败，也允许用户使用本地登录
                    _this5.isLogged = true;
                    uni.showToast({
                      title: '本地登录成功，但无法连接服务器',
                      icon: 'none',
                      duration: 2000
                    });
                  case 21:
                    _context3.next = 27;
                    break;
                  case 23:
                    _context3.prev = 23;
                    _context3.t1 = _context3["catch"](0);
                    console.error('登录过程出现异常:', _context3.t1);
                    uni.showToast({
                      title: '登录处理失败',
                      icon: 'none'
                    });
                  case 27:
                    _context3.prev = 27;
                    // 关闭模态框
                    _this5.closeLoginModal();
                    uni.hideLoading();
                    return _context3.finish(27);
                  case 31:
                  case "end":
                    return _context3.stop();
                }
              }
            }, _callee3, null, [[0, 23, 27, 31], [8, 16]]);
          }));
          function success(_x) {
            return _success.apply(this, arguments);
          }
          return success;
        }(),
        fail: function fail(err) {
          console.error('获取微信code失败:', err);
          uni.hideLoading();
          uni.showToast({
            title: '微信登录失败',
            icon: 'none'
          });
        }
      });
    },
    handleFunction: function handleFunction(item) {
      var routeMap = {
        'info': '/pages/mine/profile',
        'notes': '/pages/mine/notes',
        'footprint': '/pages/footprint/footprint',
        'feedback': '/pages/mine/feedback'
      };
      if (routeMap[item.type]) {
        uni.navigateTo({
          url: routeMap[item.type]
        });
      } else {
        uni.showToast({
          title: "".concat(item.label, "\u529F\u80FD\u5F00\u53D1\u4E2D"),
          icon: 'none'
        });
      }
    },
    getStatIcon: function getStatIcon(label) {
      var iconMap = {
        '粉丝': 'person',
        '获赞': 'heart',
        '关注': 'eye',
        '收藏': 'star'
      };
      return iconMap[label] || 'help';
    },
    onChooseAvatar: function onChooseAvatar(e) {
      console.log('选择头像:', e.detail);
      this.tempAvatarUrl = e.detail.avatarUrl;
    },
    onInputNickname: function onInputNickname(e) {
      console.log('输入昵称:', e.detail.value);
      this.tempNickName = e.detail.value;
    },
    saveUserInfo: function saveUserInfo() {
      if (!this.tempNickName.trim()) {
        uni.showToast({
          title: '请输入昵称',
          icon: 'none'
        });
        return;
      }
      if (!this.tempAvatarUrl) {
        uni.showToast({
          title: '请选择头像',
          icon: 'none'
        });
        return;
      }
      console.log('保存用户信息:', this.tempAvatarUrl, this.tempNickName);

      // 创建自定义用户信息对象
      var customUserInfo = {
        nickName: this.tempNickName,
        avatarUrl: this.tempAvatarUrl,
        gender: 0,
        country: '',
        province: '',
        city: '',
        language: 'zh_CN'
      };

      // 保存到本地存储
      uni.setStorageSync('wx_user_info', customUserInfo);

      // 调用登录方法
      this.loginWithWechat(customUserInfo);
    },
    handleLoginSuccess: function handleLoginSuccess(data) {
      console.log('收到登录成功事件', data);
      if (data && data.userInfo) {
        // 直接使用事件传递的用户信息更新页面状态
        this.avatarUrl = data.userInfo.avatar || data.userInfo.avatarUrl || '';
        this.nickName = data.userInfo.nickname || data.userInfo.nickName || '';
        this.isLogged = true;
        console.log('通过事件更新用户信息:', {
          头像: this.avatarUrl,
          昵称: this.nickName
        });

        // 如果事件包含token，确保也保存到本地存储
        if (data.token) {
          console.log('从事件中获取并保存token');
          uni.setStorageSync('token', data.token);
        } else {
          // 如果没有传递token但确认登录成功，创建一个临时token
          var tempToken = 'temp_' + new Date().getTime();
          uni.setStorageSync('token', tempToken);
          console.log('事件中没有token，创建临时token:', tempToken);
        }

        // 加载用户统计数据
        this.loadUserStatsData();
      } else {
        // 如果没有传递用户信息，则重新检查登录状态
        this.checkLoginStatus();
      }
    },
    handleLoginStatusChanged: function handleLoginStatusChanged(data) {
      console.log('收到登录状态变化事件', data);
      if (data && data.userInfo) {
        // 直接使用事件传递的用户信息更新页面状态
        this.avatarUrl = data.userInfo.avatar || data.userInfo.avatarUrl || '';
        this.nickName = data.userInfo.nickname || data.userInfo.nickName || '';
        this.isLogged = true;
        console.log('通过事件更新用户信息:', {
          头像: this.avatarUrl,
          昵称: this.nickName
        });

        // 如果事件包含token，确保也保存到本地存储
        if (data.token) {
          console.log('从状态变化事件中获取并保存token');
          uni.setStorageSync('token', data.token);
        }

        // 加载用户统计数据
        this.loadUserStatsData();
      } else {
        // 如果没有传递用户信息，则重新检查登录状态
        this.checkLoginStatus();
      }
    },
    // 刷新登录状态的方法，可以在需要时调用
    refreshLoginStatus: function refreshLoginStatus() {
      console.log("主动刷新登录状态...");

      // 先清除当前页面状态
      this.isLogged = false;
      this.avatarUrl = '';
      this.nickName = '';

      // 获取存储中最新的数据
      var token = uni.getStorageSync('token');
      var userInfo = uni.getStorageSync('userInfo');
      if (token && userInfo) {
        console.log("刷新状态: 找到有效的token和用户信息");
        // 更新页面状态
        this.avatarUrl = userInfo.avatar || userInfo.avatarUrl || '';
        this.nickName = userInfo.nickname || userInfo.nickName || '';
        this.isLogged = true;

        // 同步更新App全局状态
        var app = getApp();
        if (app && app.globalData) {
          app.globalData.isLoggedIn = true;
          app.globalData.userInfo = userInfo;
        }
        return true;
      } else {
        console.log("刷新状态: 未找到有效的登录信息");
        return false;
      }
    }
  }
};
exports.default = _default;
/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! ./node_modules/@dcloudio/uni-mp-weixin/dist/wx.js */ 1)["default"], __webpack_require__(/*! ./node_modules/@dcloudio/uni-mp-weixin/dist/index.js */ 2)["default"]))

/***/ }),

/***/ 78:
/*!****************************************************************************************!*\
  !*** I:/基于在线评论的旅游景点智能推荐系统/小程序/前端/pages/mine/mine.vue?vue&type=style&index=0&lang=css& ***!
  \****************************************************************************************/
/*! no static exports found */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _HBuilderX_plugins_uniapp_cli_node_modules_mini_css_extract_plugin_dist_loader_js_ref_6_oneOf_1_0_HBuilderX_plugins_uniapp_cli_node_modules_css_loader_dist_cjs_js_ref_6_oneOf_1_1_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_loaders_stylePostLoader_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_6_oneOf_1_2_HBuilderX_plugins_uniapp_cli_node_modules_postcss_loader_src_index_js_ref_6_oneOf_1_3_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_mine_vue_vue_type_style_index_0_lang_css___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/mini-css-extract-plugin/dist/loader.js??ref--6-oneOf-1-0!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/css-loader/dist/cjs.js??ref--6-oneOf-1-1!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/vue-cli-plugin-uni/packages/vue-loader/lib/loaders/stylePostLoader.js!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/vue-cli-plugin-uni/packages/webpack-preprocess-loader??ref--6-oneOf-1-2!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/postcss-loader/src??ref--6-oneOf-1-3!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/vue-cli-plugin-uni/packages/vue-loader/lib??vue-loader-options!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/webpack-uni-mp-loader/lib/style.js!./mine.vue?vue&type=style&index=0&lang=css& */ 79);
/* harmony import */ var _HBuilderX_plugins_uniapp_cli_node_modules_mini_css_extract_plugin_dist_loader_js_ref_6_oneOf_1_0_HBuilderX_plugins_uniapp_cli_node_modules_css_loader_dist_cjs_js_ref_6_oneOf_1_1_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_loaders_stylePostLoader_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_6_oneOf_1_2_HBuilderX_plugins_uniapp_cli_node_modules_postcss_loader_src_index_js_ref_6_oneOf_1_3_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_mine_vue_vue_type_style_index_0_lang_css___WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_HBuilderX_plugins_uniapp_cli_node_modules_mini_css_extract_plugin_dist_loader_js_ref_6_oneOf_1_0_HBuilderX_plugins_uniapp_cli_node_modules_css_loader_dist_cjs_js_ref_6_oneOf_1_1_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_loaders_stylePostLoader_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_6_oneOf_1_2_HBuilderX_plugins_uniapp_cli_node_modules_postcss_loader_src_index_js_ref_6_oneOf_1_3_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_mine_vue_vue_type_style_index_0_lang_css___WEBPACK_IMPORTED_MODULE_0__);
/* harmony reexport (unknown) */ for(var __WEBPACK_IMPORT_KEY__ in _HBuilderX_plugins_uniapp_cli_node_modules_mini_css_extract_plugin_dist_loader_js_ref_6_oneOf_1_0_HBuilderX_plugins_uniapp_cli_node_modules_css_loader_dist_cjs_js_ref_6_oneOf_1_1_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_loaders_stylePostLoader_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_6_oneOf_1_2_HBuilderX_plugins_uniapp_cli_node_modules_postcss_loader_src_index_js_ref_6_oneOf_1_3_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_mine_vue_vue_type_style_index_0_lang_css___WEBPACK_IMPORTED_MODULE_0__) if(["default"].indexOf(__WEBPACK_IMPORT_KEY__) < 0) (function(key) { __webpack_require__.d(__webpack_exports__, key, function() { return _HBuilderX_plugins_uniapp_cli_node_modules_mini_css_extract_plugin_dist_loader_js_ref_6_oneOf_1_0_HBuilderX_plugins_uniapp_cli_node_modules_css_loader_dist_cjs_js_ref_6_oneOf_1_1_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_loaders_stylePostLoader_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_6_oneOf_1_2_HBuilderX_plugins_uniapp_cli_node_modules_postcss_loader_src_index_js_ref_6_oneOf_1_3_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_mine_vue_vue_type_style_index_0_lang_css___WEBPACK_IMPORTED_MODULE_0__[key]; }) }(__WEBPACK_IMPORT_KEY__));
 /* harmony default export */ __webpack_exports__["default"] = (_HBuilderX_plugins_uniapp_cli_node_modules_mini_css_extract_plugin_dist_loader_js_ref_6_oneOf_1_0_HBuilderX_plugins_uniapp_cli_node_modules_css_loader_dist_cjs_js_ref_6_oneOf_1_1_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_loaders_stylePostLoader_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_6_oneOf_1_2_HBuilderX_plugins_uniapp_cli_node_modules_postcss_loader_src_index_js_ref_6_oneOf_1_3_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_mine_vue_vue_type_style_index_0_lang_css___WEBPACK_IMPORTED_MODULE_0___default.a); 

/***/ }),

/***/ 79:
/*!********************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/mini-css-extract-plugin/dist/loader.js??ref--6-oneOf-1-0!./node_modules/css-loader/dist/cjs.js??ref--6-oneOf-1-1!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/webpack-preprocess-loader??ref--6-oneOf-1-2!./node_modules/postcss-loader/src??ref--6-oneOf-1-3!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/vue-loader/lib??vue-loader-options!./node_modules/@dcloudio/webpack-uni-mp-loader/lib/style.js!I:/基于在线评论的旅游景点智能推荐系统/小程序/前端/pages/mine/mine.vue?vue&type=style&index=0&lang=css& ***!
  \********************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

// extracted by mini-css-extract-plugin
    if(false) { var cssReload; }
  

/***/ })

},[[72,"common/runtime","common/vendor"]]]);
//# sourceMappingURL=../../../.sourcemap/mp-weixin/pages/mine/mine.js.map