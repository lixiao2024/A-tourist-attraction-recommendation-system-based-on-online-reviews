(global["webpackJsonp"] = global["webpackJsonp"] || []).push([["pages/detail/detail"],{

/***/ 56:
/*!******************************************************************************!*\
  !*** I:/基于在线评论的旅游景点智能推荐系统/小程序/前端/main.js?{"page":"pages%2Fdetail%2Fdetail"} ***!
  \******************************************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";
/* WEBPACK VAR INJECTION */(function(wx, createPage) {

var _interopRequireDefault = __webpack_require__(/*! @babel/runtime/helpers/interopRequireDefault */ 4);
__webpack_require__(/*! uni-pages */ 26);
__webpack_require__(/*! @dcloudio/vue-cli-plugin-uni/packages/uni-cloud/dist/index.js */ 27);
var _vue = _interopRequireDefault(__webpack_require__(/*! vue */ 25));
var _detail = _interopRequireDefault(__webpack_require__(/*! ./pages/detail/detail.vue */ 57));
// @ts-ignore
wx.__webpack_require_UNI_MP_PLUGIN__ = __webpack_require__;
createPage(_detail.default);
/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! ./node_modules/@dcloudio/uni-mp-weixin/dist/wx.js */ 1)["default"], __webpack_require__(/*! ./node_modules/@dcloudio/uni-mp-weixin/dist/index.js */ 2)["createPage"]))

/***/ }),

/***/ 57:
/*!***********************************************************!*\
  !*** I:/基于在线评论的旅游景点智能推荐系统/小程序/前端/pages/detail/detail.vue ***!
  \***********************************************************/
/*! no static exports found */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _detail_vue_vue_type_template_id_3e159eb4___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./detail.vue?vue&type=template&id=3e159eb4& */ 58);
/* harmony import */ var _detail_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./detail.vue?vue&type=script&lang=js& */ 60);
/* harmony reexport (unknown) */ for(var __WEBPACK_IMPORT_KEY__ in _detail_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__) if(["default"].indexOf(__WEBPACK_IMPORT_KEY__) < 0) (function(key) { __webpack_require__.d(__webpack_exports__, key, function() { return _detail_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__[key]; }) }(__WEBPACK_IMPORT_KEY__));
/* harmony import */ var _detail_vue_vue_type_style_index_0_lang_scss___WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./detail.vue?vue&type=style&index=0&lang=scss& */ 62);
/* harmony import */ var _HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_runtime_componentNormalizer_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/vue-cli-plugin-uni/packages/vue-loader/lib/runtime/componentNormalizer.js */ 44);

var renderjs





/* normalize component */

var component = Object(_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_runtime_componentNormalizer_js__WEBPACK_IMPORTED_MODULE_3__["default"])(
  _detail_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__["default"],
  _detail_vue_vue_type_template_id_3e159eb4___WEBPACK_IMPORTED_MODULE_0__["render"],
  _detail_vue_vue_type_template_id_3e159eb4___WEBPACK_IMPORTED_MODULE_0__["staticRenderFns"],
  false,
  null,
  null,
  null,
  false,
  _detail_vue_vue_type_template_id_3e159eb4___WEBPACK_IMPORTED_MODULE_0__["components"],
  renderjs
)

component.options.__file = "pages/detail/detail.vue"
/* harmony default export */ __webpack_exports__["default"] = (component.exports);

/***/ }),

/***/ 58:
/*!******************************************************************************************!*\
  !*** I:/基于在线评论的旅游景点智能推荐系统/小程序/前端/pages/detail/detail.vue?vue&type=template&id=3e159eb4& ***!
  \******************************************************************************************/
/*! exports provided: render, staticRenderFns, recyclableRender, components */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_loaders_templateLoader_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_17_0_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_template_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_uni_app_loader_page_meta_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_detail_vue_vue_type_template_id_3e159eb4___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/vue-cli-plugin-uni/packages/vue-loader/lib/loaders/templateLoader.js??vue-loader-options!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/vue-cli-plugin-uni/packages/webpack-preprocess-loader??ref--17-0!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/webpack-uni-mp-loader/lib/template.js!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/vue-cli-plugin-uni/packages/webpack-uni-app-loader/page-meta.js!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/vue-cli-plugin-uni/packages/vue-loader/lib??vue-loader-options!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/webpack-uni-mp-loader/lib/style.js!./detail.vue?vue&type=template&id=3e159eb4& */ 59);
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "render", function() { return _HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_loaders_templateLoader_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_17_0_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_template_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_uni_app_loader_page_meta_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_detail_vue_vue_type_template_id_3e159eb4___WEBPACK_IMPORTED_MODULE_0__["render"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "staticRenderFns", function() { return _HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_loaders_templateLoader_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_17_0_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_template_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_uni_app_loader_page_meta_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_detail_vue_vue_type_template_id_3e159eb4___WEBPACK_IMPORTED_MODULE_0__["staticRenderFns"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "recyclableRender", function() { return _HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_loaders_templateLoader_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_17_0_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_template_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_uni_app_loader_page_meta_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_detail_vue_vue_type_template_id_3e159eb4___WEBPACK_IMPORTED_MODULE_0__["recyclableRender"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "components", function() { return _HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_loaders_templateLoader_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_17_0_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_template_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_uni_app_loader_page_meta_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_detail_vue_vue_type_template_id_3e159eb4___WEBPACK_IMPORTED_MODULE_0__["components"]; });



/***/ }),

/***/ 59:
/*!******************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/@dcloudio/vue-cli-plugin-uni/packages/vue-loader/lib/loaders/templateLoader.js??vue-loader-options!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/webpack-preprocess-loader??ref--17-0!./node_modules/@dcloudio/webpack-uni-mp-loader/lib/template.js!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/webpack-uni-app-loader/page-meta.js!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/vue-loader/lib??vue-loader-options!./node_modules/@dcloudio/webpack-uni-mp-loader/lib/style.js!I:/基于在线评论的旅游景点智能推荐系统/小程序/前端/pages/detail/detail.vue?vue&type=template&id=3e159eb4& ***!
  \******************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************/
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
      return Promise.all(/*! import() | uni_modules/uni-icons/components/uni-icons/uni-icons */[__webpack_require__.e("common/vendor"), __webpack_require__.e("uni_modules/uni-icons/components/uni-icons/uni-icons")]).then(__webpack_require__.bind(null, /*! @/uni_modules/uni-icons/components/uni-icons/uni-icons.vue */ 136))
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
  var g0 = _vm.isDataLoaded
    ? _vm.detail.images && _vm.detail.images.length > 0
    : null
  var g1 = _vm.replies.length
  var g2 = !_vm.hasMore && _vm.replies.length > 0
  var g3 = _vm.showCommentBox ? _vm.replyContent.length : null
  var g4 = _vm.showCommentBox ? _vm.replyContent.trim().length : null
  var g5 = _vm.showCommentBox ? _vm.replyContent.trim().length : null
  if (!_vm._isMounted) {
    _vm.e0 = function ($event, reply) {
      var _temp = arguments[arguments.length - 1].currentTarget.dataset,
        _temp2 = _temp.eventParams || _temp["event-params"],
        reply = _temp2.reply
      var _temp, _temp2
      _vm.replyHoverId = reply.id
    }
    _vm.e1 = function ($event) {
      _vm.replyHoverId = null
    }
  }
  _vm.$mp.data = Object.assign(
    {},
    {
      $root: {
        g0: g0,
        g1: g1,
        g2: g2,
        g3: g3,
        g4: g4,
        g5: g5,
      },
    }
  )
}
var recyclableRender = false
var staticRenderFns = []
render._withStripped = true



/***/ }),

/***/ 60:
/*!************************************************************************************!*\
  !*** I:/基于在线评论的旅游景点智能推荐系统/小程序/前端/pages/detail/detail.vue?vue&type=script&lang=js& ***!
  \************************************************************************************/
/*! no static exports found */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _HBuilderX_plugins_uniapp_cli_node_modules_babel_loader_lib_index_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_13_1_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_script_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_detail_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/babel-loader/lib!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/vue-cli-plugin-uni/packages/webpack-preprocess-loader??ref--13-1!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/webpack-uni-mp-loader/lib/script.js!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/vue-cli-plugin-uni/packages/vue-loader/lib??vue-loader-options!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/webpack-uni-mp-loader/lib/style.js!./detail.vue?vue&type=script&lang=js& */ 61);
/* harmony import */ var _HBuilderX_plugins_uniapp_cli_node_modules_babel_loader_lib_index_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_13_1_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_script_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_detail_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_HBuilderX_plugins_uniapp_cli_node_modules_babel_loader_lib_index_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_13_1_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_script_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_detail_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__);
/* harmony reexport (unknown) */ for(var __WEBPACK_IMPORT_KEY__ in _HBuilderX_plugins_uniapp_cli_node_modules_babel_loader_lib_index_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_13_1_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_script_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_detail_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__) if(["default"].indexOf(__WEBPACK_IMPORT_KEY__) < 0) (function(key) { __webpack_require__.d(__webpack_exports__, key, function() { return _HBuilderX_plugins_uniapp_cli_node_modules_babel_loader_lib_index_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_13_1_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_script_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_detail_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__[key]; }) }(__WEBPACK_IMPORT_KEY__));
 /* harmony default export */ __webpack_exports__["default"] = (_HBuilderX_plugins_uniapp_cli_node_modules_babel_loader_lib_index_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_13_1_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_script_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_detail_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0___default.a); 

/***/ }),

/***/ 61:
/*!*******************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/babel-loader/lib!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/webpack-preprocess-loader??ref--13-1!./node_modules/@dcloudio/webpack-uni-mp-loader/lib/script.js!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/vue-loader/lib??vue-loader-options!./node_modules/@dcloudio/webpack-uni-mp-loader/lib/style.js!I:/基于在线评论的旅游景点智能推荐系统/小程序/前端/pages/detail/detail.vue?vue&type=script&lang=js& ***!
  \*******************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************/
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
var _toConsumableArray2 = _interopRequireDefault(__webpack_require__(/*! @babel/runtime/helpers/toConsumableArray */ 18));
var _asyncToGenerator2 = _interopRequireDefault(__webpack_require__(/*! @babel/runtime/helpers/asyncToGenerator */ 31));
var _api = __webpack_require__(/*! @/request/api.js */ 52);
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
  // 移除不必要的配置，使用pages.json中的配置
  data: function data() {
    return {
      commentId: null,
      contentType: 'comment',
      // 初始化空对象，避免渲染时获取不到属性
      detail: {
        id: 0,
        avatar: '/static/default-avatar.png',
        nickname: '',
        content: '',
        publishTime: '',
        likeCount: 0,
        commentCount: 0,
        collectCount: 0,
        isLiked: false,
        isCollected: false,
        isFollowed: false
      },
      replies: [],
      page: 1,
      pageSize: 10,
      hasMore: true,
      loading: false,
      isDataLoaded: false,
      isRefreshing: false,
      showCommentBox: false,
      replyContent: '',
      replyPlaceholder: '写下你的评论...',
      replyHoverId: null,
      replyToUser: null,
      // 回复某个具体用户
      showLoginPopup: false,
      // 登录弹窗显示状态
      actionAfterLogin: null,
      // 登录后要执行的动作
      isLoggedIn: false,
      // 新增的登录状态
      // 新增登录相关的状态
      loginStep: 1,
      canIUseGetUserProfile: false,
      tempAvatarUrl: '',
      tempNickName: ''
    };
  },
  // 响应导航栏按钮点击
  onNavigationBarButtonTap: function onNavigationBarButtonTap(e) {
    this.shareComment();
  },
  onLoad: function onLoad(options) {
    // 获取传递的评论ID参数
    this.commentId = options.id || null;
    // 获取传递的类型参数（评论或笔记）
    this.contentType = options.type || 'comment';

    // 检查是否支持getUserProfile
    if (wx.getUserProfile) {
      this.canIUseGetUserProfile = true;
    }

    // 尝试从App全局状态获取登录信息
    var app = getApp();
    if (app.globalData && app.globalData.isLoggedIn) {
      console.log('从App全局状态获取登录信息');
      this.isLoggedIn = true;
    }

    // 添加登录状态变化监听
    uni.$on('loginStatusChanged', this.handleLoginStatusChanged);
    if (this.contentType === 'note') {
      // 从本地存储获取笔记数据
      this.loadNoteData();
    } else {
      // 正常加载评论数据
      this.initData();
    }
  },
  // 在页面卸载时移除事件监听
  onUnload: function onUnload() {
    uni.$off('loginStatusChanged', this.handleLoginStatusChanged);
  },
  methods: {
    // 加载笔记数据
    loadNoteData: function loadNoteData() {
      try {
        // 显示加载中
        uni.showLoading({
          title: '加载中...',
          mask: true
        });

        // 从本地存储获取当前笔记
        var noteData = uni.getStorageSync('currentNote');
        if (noteData) {
          var _uni$getStorageSync;
          // 处理图片URL，确保URL正确
          var images = [];
          if (noteData.images && noteData.images.length > 0) {
            images = noteData.images.filter(function (img) {
              return img && typeof img === 'string';
            });
            console.log('处理后的图片数组:', images);
          }

          // 格式化笔记数据为详情页需要的格式
          this.detail = {
            id: noteData.id,
            avatar: noteData.avatar || '/static/default-avatar.png',
            nickname: ((_uni$getStorageSync = uni.getStorageSync('userInfo')) === null || _uni$getStorageSync === void 0 ? void 0 : _uni$getStorageSync.nickname) || '匿名用户',
            content: noteData.content,
            publishTime: noteData.createTime,
            likeCount: noteData.likeCount || 0,
            commentCount: noteData.commentCount || 0,
            isLiked: noteData.isLiked || false,
            isCollected: noteData.isCollected || false,
            isFollowed: false,
            images: images
          };

          // 如果有评论数据，加载评论
          if (noteData.replies && noteData.replies.length > 0) {
            this.replies = noteData.replies;
            this.hasMore = false;
          } else {
            this.replies = [];
            this.hasMore = false;
          }
          this.isDataLoaded = true;
        } else {
          uni.showToast({
            title: '笔记不存在',
            icon: 'none'
          });

          // 延迟返回
          setTimeout(function () {
            uni.navigateBack({
              fail: function fail() {
                // 如果返回失败，则跳转到我的页面
                uni.switchTab({
                  url: '/pages/mine/mine'
                });
              }
            });
          }, 1500);
        }
      } catch (error) {
        console.error('加载笔记数据失败:', error);
        uni.showToast({
          title: '加载失败',
          icon: 'none'
        });
      } finally {
        uni.hideLoading();
      }
    },
    // 初始化数据
    initData: function initData() {
      var _this = this;
      return (0, _asyncToGenerator2.default)( /*#__PURE__*/_regenerator.default.mark(function _callee() {
        var postDetail, isLoggedIn, _postDetail$user, _postDetail$user2;
        return _regenerator.default.wrap(function _callee$(_context) {
          while (1) {
            switch (_context.prev = _context.next) {
              case 0:
                if (!_this.isDataLoaded) {
                  _context.next = 2;
                  break;
                }
                return _context.abrupt("return");
              case 2:
                if (_this.commentId) {
                  _context.next = 5;
                  break;
                }
                uni.showToast({
                  title: '参数错误',
                  icon: 'none'
                });
                return _context.abrupt("return");
              case 5:
                _context.prev = 5;
                uni.showLoading({
                  title: '加载中...',
                  mask: true
                });

                // 加载评论详情
                if (!_this.commentId) {
                  _context.next = 31;
                  break;
                }
                _context.prev = 8;
                _context.next = 11;
                return (0, _api.getPostDetail)(_this.commentId);
              case 11:
                postDetail = _context.sent;
                console.log('获取到的帖子详情:', postDetail);

                // 检查用户是否已登录
                isLoggedIn = !!uni.getStorageSync('token');
                _this.isLoggedIn = isLoggedIn;
                if (!(postDetail && postDetail.id)) {
                  _context.next = 22;
                  break;
                }
                // 转换数据格式以适应前端展示
                _this.detail = {
                  id: postDetail.id,
                  avatar: ((_postDetail$user = postDetail.user) === null || _postDetail$user === void 0 ? void 0 : _postDetail$user.avatar) || '/static/default-avatar.png',
                  nickname: ((_postDetail$user2 = postDetail.user) === null || _postDetail$user2 === void 0 ? void 0 : _postDetail$user2.nickname) || '旅行达人',
                  content: postDetail.content || '内容获取失败',
                  publishTime: _this.formatPublishTime(postDetail.created_at) || '未知时间',
                  likeCount: postDetail.likes_count || 0,
                  commentCount: postDetail.comments_count || 0,
                  collectCount: postDetail.collects_count || 0,
                  isLiked: false,
                  isCollected: false,
                  isFollowed: false,
                  images: postDetail.images || []
                };

                // 加载评论回复
                _context.next = 19;
                return _this.loadCommentReplies();
              case 19:
                // 设置用户交互状态
                if (isLoggedIn) {
                  _this.checkUserInteractions();
                }
                _context.next = 24;
                break;
              case 22:
                _context.next = 24;
                return _this.loadMockData();
              case 24:
                _context.next = 31;
                break;
              case 26:
                _context.prev = 26;
                _context.t0 = _context["catch"](8);
                console.error('API请求失败:', _context.t0);
                // API请求失败时，加载模拟数据
                _context.next = 31;
                return _this.loadMockData();
              case 31:
                _this.isDataLoaded = true;
                _context.next = 38;
                break;
              case 34:
                _context.prev = 34;
                _context.t1 = _context["catch"](5);
                console.error('初始化数据失败:', _context.t1);
                uni.showToast({
                  title: '加载失败，请重试',
                  icon: 'none'
                });
              case 38:
                _context.prev = 38;
                uni.hideLoading();
                return _context.finish(38);
              case 41:
              case "end":
                return _context.stop();
            }
          }
        }, _callee, null, [[5, 34, 38, 41], [8, 26]]);
      }))();
    },
    // 加载模拟数据（当API请求失败时使用）
    loadMockData: function loadMockData() {
      var _this2 = this;
      return (0, _asyncToGenerator2.default)( /*#__PURE__*/_regenerator.default.mark(function _callee2() {
        return _regenerator.default.wrap(function _callee2$(_context2) {
          while (1) {
            switch (_context2.prev = _context2.next) {
              case 0:
                _context2.next = 2;
                return Promise.all([_this2.loadCommentDetail(), _this2.loadCommentReplies()]);
              case 2:
              case "end":
                return _context2.stop();
            }
          }
        }, _callee2);
      }))();
    },
    // 格式化发布时间
    formatPublishTime: function formatPublishTime(timeStr) {
      if (!timeStr) return '未知时间';
      var publishTime = new Date(timeStr);
      var now = new Date();
      var diffMs = now - publishTime;
      var diffSec = Math.floor(diffMs / 1000);
      var diffMin = Math.floor(diffSec / 60);
      var diffHour = Math.floor(diffMin / 60);
      var diffDay = Math.floor(diffHour / 24);
      if (diffSec < 60) {
        return '刚刚';
      } else if (diffMin < 60) {
        return "".concat(diffMin, "\u5206\u949F\u524D");
      } else if (diffHour < 24) {
        return "".concat(diffHour, "\u5C0F\u65F6\u524D");
      } else if (diffDay < 30) {
        return "".concat(diffDay, "\u5929\u524D");
      } else {
        // 返回具体日期，如 2023-05-01
        return publishTime.toISOString().split('T')[0];
      }
    },
    // 加载评论详情
    loadCommentDetail: function loadCommentDetail() {
      var _this3 = this;
      return new Promise(function (resolve) {
        // 模拟API请求，实际项目中应替换为真实接口调用
        console.log('加载评论ID:', _this3.commentId);
        setTimeout(function () {
          // 这里模拟根据ID获取不同的评论详情
          if (_this3.commentId == 2) {
            _this3.detail = {
              id: 2,
              avatar: '/static/default-avatar.png',
              nickname: '游客007',
              content: '一般般，人太多',
              publishTime: '5小时前',
              likeCount: 5,
              commentCount: 2,
              collectCount: 1,
              isLiked: false,
              isCollected: false,
              isFollowed: false
            };
          } else {
            // 其他ID使用默认数据
            _this3.detail = {
              id: 1,
              avatar: '/static/default-avatar.png',
              nickname: '旅行达人',
              content: '这个景点非常值得一去，尤其是日落时分的景色美不胜收！建议下午4点时到达，可以慢慢欣赏天色变化。',
              publishTime: '3小时前',
              likeCount: 12,
              commentCount: 5,
              collectCount: 3,
              isLiked: false,
              isCollected: false,
              isFollowed: false
            };
          }

          // 数据加载完成
          resolve();
        }, 300);
      });
    },
    // 加载评论回复
    loadCommentReplies: function loadCommentReplies() {
      var _this4 = this;
      if (this.loading || !this.hasMore) return Promise.resolve();
      this.loading = true;
      return new Promise( /*#__PURE__*/function () {
        var _ref = (0, _asyncToGenerator2.default)( /*#__PURE__*/_regenerator.default.mark(function _callee3(resolve) {
          var skip, comments, formattedComments;
          return _regenerator.default.wrap(function _callee3$(_context3) {
            while (1) {
              switch (_context3.prev = _context3.next) {
                case 0:
                  _context3.prev = 0;
                  if (!(_this4.contentType === 'note')) {
                    _context3.next = 6;
                    break;
                  }
                  _context3.next = 4;
                  return _this4.loadReplies();
                case 4:
                  resolve();
                  return _context3.abrupt("return");
                case 6:
                  // 从服务器获取评论
                  skip = (_this4.page - 1) * _this4.pageSize;
                  _context3.next = 9;
                  return (0, _api.getComments)(_this4.commentId, _this4.page, _this4.pageSize);
                case 9:
                  comments = _context3.sent;
                  if (Array.isArray(comments) && comments.length > 0) {
                    // 格式化评论数据
                    formattedComments = comments.map(function (comment) {
                      var _comment$user, _comment$user2;
                      return {
                        id: comment.id,
                        avatar: ((_comment$user = comment.user) === null || _comment$user === void 0 ? void 0 : _comment$user.avatar) || '/static/default-avatar.png',
                        nickname: ((_comment$user2 = comment.user) === null || _comment$user2 === void 0 ? void 0 : _comment$user2.nickname) || '游客',
                        content: comment.content,
                        publishTime: _this4.formatPublishTime(comment.created_at),
                        likeCount: 0,
                        // 暂不支持评论点赞
                        isLiked: false
                      };
                    }); // 如果是第一页，替换评论列表；否则追加
                    if (_this4.page === 1) {
                      _this4.replies = formattedComments;
                    } else {
                      _this4.replies = [].concat((0, _toConsumableArray2.default)(_this4.replies), (0, _toConsumableArray2.default)(formattedComments));
                    }

                    // 更新页码和状态
                    _this4.page++;
                    _this4.hasMore = comments.length >= _this4.pageSize;
                  } else {
                    // 没有更多评论了
                    if (_this4.page > 1) {
                      _this4.hasMore = false;
                    } else if (_this4.page === 1) {
                      // 第一页就没有数据
                      _this4.replies = [];
                      _this4.hasMore = false;
                    }
                  }
                  _context3.next = 18;
                  break;
                case 13:
                  _context3.prev = 13;
                  _context3.t0 = _context3["catch"](0);
                  console.error('获取评论列表失败:', _context3.t0);
                  // 如果API请求失败，回退到模拟数据
                  _context3.next = 18;
                  return _this4.loadReplies();
                case 18:
                  _context3.prev = 18;
                  _this4.loading = false;
                  resolve();
                  return _context3.finish(18);
                case 22:
                case "end":
                  return _context3.stop();
              }
            }
          }, _callee3, null, [[0, 13, 18, 22]]);
        }));
        return function (_x) {
          return _ref.apply(this, arguments);
        };
      }());
    },
    // 备用方法：加载模拟评论数据
    loadReplies: function loadReplies() {
      var _this5 = this;
      return new Promise(function (resolve) {
        // 模拟API请求延迟
        setTimeout(function () {
          // 模拟分页数据
          if (_this5.commentId == 2) {
            // 为ID为2的评论添加特定回复
            if (_this5.page === 1) {
              _this5.replies = [{
                id: 2,
                avatar: '/static/default-avatar.png',
                nickname: '本地用户',
                content: '同意，周末人确实很多',
                publishTime: '2小时前',
                likeCount: 3,
                isLiked: false
              }];
            } else {
              // 第二页没有更多数据
              _this5.hasMore = false;
            }
          } else if (_this5.page === 1) {
            // 第一页数据
            _this5.replies = [{
              id: 1,
              avatar: '/static/default-avatar.png',
              nickname: '用户A',
              content: '感谢分享！周末就去看看',
              publishTime: '1小时前',
              likeCount: 5,
              isLiked: false
            }];
          } else if (_this5.page > 1) {
            // 为其他评论ID模拟加载更多数据
            var moreReplies = [{
              id: _this5.replies.length + 1,
              avatar: '/static/default-avatar.png',
              nickname: '用户' + (_this5.page + 1),
              content: '这是加载的第' + _this5.page + '页回复',
              publishTime: Math.floor(Math.random() * 24) + '小时前',
              likeCount: Math.floor(Math.random() * 10),
              isLiked: false
            }];
            _this5.replies = [].concat((0, _toConsumableArray2.default)(_this5.replies), moreReplies);

            // 模拟数据到第3页结束
            if (_this5.page >= 3) {
              _this5.hasMore = false;
            }
          }
          _this5.page++;
          _this5.loading = false;
          resolve();
        }, 500);
      });
    },
    // 刷新评论
    refreshComments: function refreshComments(e) {
      var _this6 = this;
      this.isRefreshing = true;
      this.page = 1;
      this.hasMore = true;
      this.replies = [];

      // 根据内容类型选择加载方法
      if (this.contentType === 'note') {
        // 刷新笔记评论
        this.loadNoteData().then(function () {
          _this6.isRefreshing = false;
          uni.stopPullDownRefresh();
          if (e && typeof e.stopPullDownRefresh === 'function') {
            e.stopPullDownRefresh();
          }
        });
      } else {
        // 刷新评论回复
        this.loadCommentReplies().then(function () {
          _this6.isRefreshing = false;
          uni.stopPullDownRefresh();
          if (e && typeof e.stopPullDownRefresh === 'function') {
            e.stopPullDownRefresh();
          }
        });
      }
    },
    // 滚动到底部加载更多
    onScrollToLower: function onScrollToLower() {
      if (!this.loading && this.hasMore) {
        this.loadCommentReplies();
      }
    },
    // 检查用户交互状态
    checkUserInteractions: function checkUserInteractions() {
      this.checkUserInteractionStatus();
    },
    // 检查用户交互状态
    checkUserInteractionStatus: function checkUserInteractionStatus() {
      // 从本地存储获取用户交互状态
      var userInfo = uni.getStorageSync('userInfo');
      if (!userInfo) return;

      // 获取用户的点赞、收藏、关注状态
      var likedPosts = uni.getStorageSync('likedPosts') || [];
      var collectedPosts = uni.getStorageSync('collectedPosts') || [];
      var followedUsers = uni.getStorageSync('followedUsers') || [];

      // 更新当前帖子状态
      this.detail.isLiked = likedPosts.includes(this.detail.id);
      this.detail.isCollected = collectedPosts.includes(this.detail.id);
      this.detail.isFollowed = followedUsers.includes(this.detail.nickname);

      // 同时检查回复的点赞状态
      var likedReplies = uni.getStorageSync('likedReplies') || [];
      this.replies.forEach(function (reply) {
        reply.isLiked = likedReplies.includes(reply.id);
      });
    },
    // 检查登录状态
    checkLoginStatus: function checkLoginStatus() {
      // 使用组件的isLoggedIn属性
      if (!this.isLoggedIn) {
        // 显示登录弹窗，而不是提示
        this.showLoginPopup = true;
        return false;
      }
      return true;
    },
    // 处理登录事件
    handleLogin: function handleLogin() {
      // 检查是否支持getUserProfile
      if (!this.canIUseGetUserProfile) {
        this.canIUseGetUserProfile = wx.getUserProfile ? true : false;
      }
      if (this.canIUseGetUserProfile) {
        this.getUserProfile();
      } else {
        // 旧版微信，需要使用open-type="getUserInfo"的按钮
        uni.showToast({
          title: '当前微信版本过低，请升级微信版本',
          icon: 'none'
        });
      }
    },
    // 获取用户个人信息
    getUserProfile: function getUserProfile() {
      var _this7 = this;
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
          _this7.tempAvatarUrl = res.userInfo.avatarUrl;
          _this7.tempNickName = res.userInfo.nickName;

          // 如果获取到的是"微信用户"或默认头像，则进入完善信息步骤
          if (res.userInfo.nickName === '微信用户' || !res.userInfo.avatarUrl) {
            console.log('获取到默认昵称或头像，进入完善信息步骤');
            _this7.loginStep = 2;
            uni.hideLoading();
          } else {
            // 否则直接使用获取到的信息登录
            // 获取到用户信息后，继续获取微信code并调用后端API
            _this7.loginWithWechat(res.userInfo);
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
    // 使用微信登录
    loginWithWechat: function loginWithWechat(userInfo) {
      var _this8 = this;
      // 获取微信code
      uni.login({
        provider: 'weixin',
        success: function () {
          var _success = (0, _asyncToGenerator2.default)( /*#__PURE__*/_regenerator.default.mark(function _callee4(loginRes) {
            var localUserInfo, backendUrl, result, data, savedToken, action, _result$data, _action;
            return _regenerator.default.wrap(function _callee4$(_context4) {
              while (1) {
                switch (_context4.prev = _context4.next) {
                  case 0:
                    _context4.prev = 0;
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

                    // 更新登录状态
                    _this8.isLoggedIn = true;

                    // 调用后端API进行登录验证
                    console.log('准备向后端发送登录请求...');

                    // 使用实际IP地址替换localhost
                    // const backendUrl = 'http://localhost:8000/api/wechat-login';
                    backendUrl = 'http://192.168.1.10:8000/api/wechat-login'; // 替换为您的实际IP
                    _context4.prev = 7;
                    _context4.next = 10;
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
                  case 10:
                    result = _context4.sent;
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
                      console.log('保存的本地userInfo:', localUserInfo);

                      // 发布全局登录成功事件，通知其他页面更新状态
                      uni.$emit('loginSuccess', {
                        isLoggedIn: true,
                        userInfo: localUserInfo,
                        token: data.access_token // 显式包含token
                      });

                      uni.showToast({
                        title: '登录成功'
                      });

                      // 如果有登录后要执行的动作，执行它
                      if (_this8.actionAfterLogin) {
                        action = _this8.actionAfterLogin;
                        _this8.actionAfterLogin = null; // 清除动作
                        setTimeout(function () {
                          action(); // 执行之前保存的动作
                        }, 500); // 延迟一下执行，避免连续操作
                      }
                    } else {
                      console.error('登录失败:', result.data);
                      uni.showToast({
                        title: ((_result$data = result.data) === null || _result$data === void 0 ? void 0 : _result$data.detail) || '登录失败',
                        icon: 'none'
                      });
                    }
                    _context4.next = 20;
                    break;
                  case 15:
                    _context4.prev = 15;
                    _context4.t0 = _context4["catch"](7);
                    console.error('登录请求异常:', _context4.t0);
                    uni.showToast({
                      title: '登录请求失败，但本地已记录',
                      icon: 'none',
                      duration: 2000
                    });

                    // 如果有登录后要执行的动作，执行它
                    if (_this8.actionAfterLogin) {
                      _action = _this8.actionAfterLogin;
                      _this8.actionAfterLogin = null; // 清除动作
                      setTimeout(function () {
                        _action(); // 执行之前保存的动作
                      }, 500); // 延迟一下执行，避免连续操作
                    }
                  case 20:
                    _context4.next = 26;
                    break;
                  case 22:
                    _context4.prev = 22;
                    _context4.t1 = _context4["catch"](0);
                    console.error('登录过程出现异常:', _context4.t1);
                    uni.showToast({
                      title: '登录处理失败',
                      icon: 'none'
                    });
                  case 26:
                    _context4.prev = 26;
                    // 关闭登录弹窗
                    _this8.showLoginPopup = false;
                    uni.hideLoading();
                    return _context4.finish(26);
                  case 30:
                  case "end":
                    return _context4.stop();
                }
              }
            }, _callee4, null, [[0, 22, 26, 30], [7, 15]]);
          }));
          function success(_x2) {
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
    // 点赞主评论
    toggleLike: function toggleLike() {
      var _this9 = this;
      var execute = function execute() {
        // 更新点赞状态
        _this9.detail.isLiked = !_this9.detail.isLiked;

        // 更新点赞数量
        if (_this9.detail.isLiked) {
          _this9.detail.likeCount++;
          _this9.updateUserStats('获赞', 1);
        } else {
          _this9.detail.likeCount--;
          _this9.updateUserStats('获赞', -1);
        }

        // 保存点赞状态到本地
        _this9.saveInteractionStatus('likedPosts', _this9.detail.id, _this9.detail.isLiked);

        // 提示用户
        uni.showToast({
          title: _this9.detail.isLiked ? '已点赞' : '已取消点赞',
          icon: 'none'
        });
      };

      // 检查登录状态
      if (!this.checkLoginStatus()) {
        // 保存要执行的操作，登录成功后执行
        this.actionAfterLogin = execute;
        return;
      }
      execute();
    },
    // 点赞回复
    toggleReplyLike: function toggleReplyLike(index) {
      var _this10 = this;
      var execute = function execute() {
        var reply = _this10.replies[index];
        if (!reply) return;

        // 更新点赞状态
        reply.isLiked = !reply.isLiked;

        // 更新点赞数量
        if (reply.likeCount === undefined) reply.likeCount = 0;
        if (reply.isLiked) {
          reply.likeCount++;
        } else {
          reply.likeCount--;
          if (reply.likeCount < 0) reply.likeCount = 0;
        }

        // 保存点赞状态到本地
        _this10.saveInteractionStatus('likedReplies', reply.id, reply.isLiked);
      };

      // 检查登录状态
      if (!this.checkLoginStatus()) {
        // 保存要执行的操作，登录成功后执行
        this.actionAfterLogin = execute;
        return;
      }
      execute();
    },
    // 收藏功能
    toggleCollect: function toggleCollect() {
      var _this11 = this;
      var execute = function execute() {
        // 更新收藏状态
        _this11.detail.isCollected = !_this11.detail.isCollected;

        // 更新收藏数量
        if (_this11.detail.isCollected) {
          _this11.detail.collectCount++;
          _this11.updateUserStats('收藏', 1);
        } else {
          _this11.detail.collectCount--;
          _this11.updateUserStats('收藏', -1);
        }

        // 保存收藏状态到本地
        _this11.saveInteractionStatus('collectedPosts', _this11.detail.id, _this11.detail.isCollected);

        // 提示用户
        uni.showToast({
          title: _this11.detail.isCollected ? '已收藏' : '已取消收藏',
          icon: 'none'
        });
      };

      // 检查登录状态
      if (!this.checkLoginStatus()) {
        // 保存要执行的操作，登录成功后执行
        this.actionAfterLogin = execute;
        return;
      }
      execute();
    },
    // 关注功能
    toggleFollow: function toggleFollow() {
      var _this12 = this;
      var execute = function execute() {
        // 更新关注状态
        _this12.detail.isFollowed = !_this12.detail.isFollowed;

        // 更新用户统计数据
        if (_this12.detail.isFollowed) {
          _this12.updateUserStats('关注', 1);
          _this12.updateAuthorStats('粉丝', 1);
        } else {
          _this12.updateUserStats('关注', -1);
          _this12.updateAuthorStats('粉丝', -1);
        }

        // 保存关注状态到本地
        _this12.saveInteractionStatus('followedUsers', _this12.detail.nickname, _this12.detail.isFollowed);

        // 提示用户
        uni.showToast({
          title: _this12.detail.isFollowed ? '已关注' : '已取消关注',
          icon: 'none'
        });
      };

      // 检查登录状态
      if (!this.checkLoginStatus()) {
        // 保存要执行的操作，登录成功后执行
        this.actionAfterLogin = execute;
        return;
      }
      execute();
    },
    // 显示评论输入框
    showCommentInput: function showCommentInput() {
      var _this13 = this;
      // 检查登录状态
      if (!this.checkLoginStatus()) {
        // 保存要执行的操作，登录成功后执行
        this.actionAfterLogin = function () {
          _this13.replyToUser = null;
          _this13.replyPlaceholder = '写下你的评论...';
          _this13.showCommentBox = true;
        };
        return;
      }
      this.replyToUser = null;
      this.replyPlaceholder = '写下你的评论...';
      this.showCommentBox = true;
    },
    // 回复特定评论
    replyToComment: function replyToComment(reply) {
      var _this14 = this;
      // 检查登录状态
      if (!this.checkLoginStatus()) {
        // 保存要执行的操作，登录成功后执行
        this.actionAfterLogin = function () {
          _this14.replyToUser = reply;
          _this14.replyPlaceholder = "\u56DE\u590D ".concat(reply.nickname, "\uFF1A");
          _this14.showCommentBox = true;
        };
        return;
      }
      this.replyToUser = reply;
      this.replyPlaceholder = "\u56DE\u590D ".concat(reply.nickname, "\uFF1A");
      this.showCommentBox = true;
    },
    // 提交评论
    submitComment: function submitComment() {
      var _this15 = this;
      return (0, _asyncToGenerator2.default)( /*#__PURE__*/_regenerator.default.mark(function _callee5() {
        var userInfo, commentData, result, noteId, newReply;
        return _regenerator.default.wrap(function _callee5$(_context5) {
          while (1) {
            switch (_context5.prev = _context5.next) {
              case 0:
                if (_this15.replyContent.trim()) {
                  _context5.next = 3;
                  break;
                }
                uni.showToast({
                  title: '评论内容不能为空',
                  icon: 'none'
                });
                return _context5.abrupt("return");
              case 3:
                _context5.prev = 3;
                // 显示加载提示
                uni.showLoading({
                  title: '发送中...',
                  mask: true
                });

                // 获取用户信息
                userInfo = uni.getStorageSync('userInfo') || {
                  nickname: '游客',
                  avatar: '/static/default-avatar.png'
                }; // 构建评论数据
                commentData = {
                  content: _this15.replyContent,
                  parent_id: _this15.replyToUser ? _this15.replyToUser.id : null
                }; // 发送评论到后端
                if (!(_this15.contentType === 'note')) {
                  _context5.next = 12;
                  break;
                }
                // 本地笔记评论，只保存在本地
                noteId = _this15.commentId;
                result = {
                  success: true,
                  id: Date.now(),
                  // 使用时间戳作为临时ID
                  created_at: new Date().toISOString(),
                  user: {
                    nickname: userInfo.nickname,
                    avatar: userInfo.avatar
                  }
                };
                _context5.next = 15;
                break;
              case 12:
                _context5.next = 14;
                return (0, _api.submitComment)(_this15.commentId, commentData);
              case 14:
                result = _context5.sent;
              case 15:
                if (result && (result.success || result.id)) {
                  // 评论成功
                  // 创建新评论对象
                  newReply = {
                    id: result.id,
                    avatar: userInfo.avatar,
                    nickname: userInfo.nickname,
                    content: _this15.replyContent,
                    publishTime: '刚刚',
                    likeCount: 0,
                    isLiked: false
                  }; // 添加到评论列表
                  _this15.replies.unshift(newReply);

                  // 更新评论数
                  _this15.detail.commentCount++;

                  // 清空输入框并隐藏
                  _this15.replyContent = '';
                  _this15.showCommentBox = false;

                  // 提示用户
                  uni.showToast({
                    title: '评论成功',
                    icon: 'success'
                  });
                } else {
                  // 评论失败
                  uni.showToast({
                    title: '评论失败，请重试',
                    icon: 'none'
                  });
                }
                _context5.next = 22;
                break;
              case 18:
                _context5.prev = 18;
                _context5.t0 = _context5["catch"](3);
                console.error('提交评论失败:', _context5.t0);
                uni.showToast({
                  title: '评论失败，请重试',
                  icon: 'none'
                });
              case 22:
                _context5.prev = 22;
                uni.hideLoading();
                return _context5.finish(22);
              case 25:
              case "end":
                return _context5.stop();
            }
          }
        }, _callee5, null, [[3, 18, 22, 25]]);
      }))();
    },
    // 分享评论
    shareComment: function shareComment() {
      uni.showShareMenu({
        withShareTicket: true,
        success: function success() {
          uni.showToast({
            title: '分享成功',
            icon: 'success'
          });
        }
      });
    },
    // 保存交互状态到本地
    saveInteractionStatus: function saveInteractionStatus(key, id, status) {
      var items = uni.getStorageSync(key) || [];
      if (status) {
        // 添加ID到列表
        if (!items.includes(id)) {
          items.push(id);
        }
      } else {
        // 从列表中移除ID
        items = items.filter(function (item) {
          return item !== id;
        });
      }
      uni.setStorageSync(key, items);
    },
    // 更新用户统计数据
    updateUserStats: function updateUserStats(type, value) {
      // 获取用户统计数据
      var statsData = uni.getStorageSync('userStatsData') || [{
        label: '粉丝',
        value: 0
      }, {
        label: '获赞',
        value: 0
      }, {
        label: '关注',
        value: 0
      }, {
        label: '收藏',
        value: 0
      }];

      // 查找并更新对应类型的统计数据
      var statItem = statsData.find(function (item) {
        return item.label === type;
      });
      if (statItem) {
        statItem.value += value;
        if (statItem.value < 0) statItem.value = 0;
      }

      // 保存更新后的统计数据
      uni.setStorageSync('userStatsData', statsData);
    },
    // 更新作者统计数据
    updateAuthorStats: function updateAuthorStats(type, value) {
      // 获取作者统计数据
      var authorStatsData = uni.getStorageSync("authorStats_".concat(this.detail.nickname)) || [{
        label: '粉丝',
        value: 0
      }, {
        label: '获赞',
        value: 0
      }];

      // 查找并更新对应类型的统计数据
      var statItem = authorStatsData.find(function (item) {
        return item.label === type;
      });
      if (statItem) {
        statItem.value += value;
        if (statItem.value < 0) statItem.value = 0;
      }

      // 保存更新后的统计数据
      uni.setStorageSync("authorStats_".concat(this.detail.nickname), authorStatsData);
    },
    // 处理图片加载错误
    handleImageError: function handleImageError(index) {
      if (this.detail.images && this.detail.images.length > index) {
        console.log('图片加载失败:', this.detail.images[index]);
        this.detail.images[index] = '/static/default-img.png';
      }
    },
    // 预览图片
    previewImage: function previewImage(current, urls) {
      uni.previewImage({
        current: current,
        urls: urls
      });
    },
    // 关闭登录弹窗
    closeLoginModal: function closeLoginModal() {
      this.showLoginPopup = false;
      // 重置登录步骤
      this.loginStep = 1;
      this.tempNickName = '';
      this.tempAvatarUrl = '';
    },
    // 选择头像
    onChooseAvatar: function onChooseAvatar(e) {
      console.log('选择头像:', e.detail.avatarUrl);
      this.tempAvatarUrl = e.detail.avatarUrl;
    },
    // 输入昵称
    onInputNickname: function onInputNickname(e) {
      console.log('输入昵称:', e.detail.value);
      this.tempNickName = e.detail.value;
    },
    // 保存用户信息
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
      console.log('保存用户信息:', this.tempNickName, this.tempAvatarUrl);

      // 创建用户信息对象
      var userInfo = {
        nickname: this.tempNickName,
        avatar: this.tempAvatarUrl,
        // 保持兼容性
        nickName: this.tempNickName,
        avatarUrl: this.tempAvatarUrl
      };

      // 保存到本地存储
      uni.setStorageSync('userInfo', userInfo);

      // 更新页面显示的用户信息
      this.isLoggedIn = true;

      // 创建一个临时token (如果没有真实的后端token)
      var tempToken = 'temp_' + new Date().getTime();
      uni.setStorageSync('token', tempToken);

      // 记录日志，确认token是否保存成功
      var savedToken = uni.getStorageSync('token');
      console.log('手动设置profile后验证token:', savedToken ? '√ 已保存' : '× 未保存');
      console.log('保存的本地userInfo:', userInfo);

      // 发布全局登录成功事件，通知其他页面更新状态
      uni.$emit('loginSuccess', {
        isLoggedIn: true,
        userInfo: userInfo,
        token: tempToken
      });

      // 关闭登录弹窗
      this.showLoginPopup = false;

      // 如果有登录后要执行的动作，执行它
      if (this.actionAfterLogin) {
        var action = this.actionAfterLogin;
        this.actionAfterLogin = null; // 清除动作
        setTimeout(function () {
          action(); // 执行之前保存的动作
        }, 500); // 延迟一下执行，避免连续操作
      }

      // 提示用户
      uni.showToast({
        title: '登录成功',
        icon: 'success'
      });
    },
    // 处理登录状态变化
    handleLoginStatusChanged: function handleLoginStatusChanged(data) {
      console.log('收到登录状态变化事件', data);
      if (data && data.isLoggedIn) {
        this.isLoggedIn = data.isLoggedIn;

        // 更新用户交互状态
        if (this.isDataLoaded) {
          this.checkUserInteractions();
        }
      }
    }
  }
};
exports.default = _default;
/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! ./node_modules/@dcloudio/uni-mp-weixin/dist/wx.js */ 1)["default"], __webpack_require__(/*! ./node_modules/@dcloudio/uni-mp-weixin/dist/index.js */ 2)["default"]))

/***/ }),

/***/ 62:
/*!*********************************************************************************************!*\
  !*** I:/基于在线评论的旅游景点智能推荐系统/小程序/前端/pages/detail/detail.vue?vue&type=style&index=0&lang=scss& ***!
  \*********************************************************************************************/
/*! no static exports found */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _HBuilderX_plugins_uniapp_cli_node_modules_mini_css_extract_plugin_dist_loader_js_ref_8_oneOf_1_0_HBuilderX_plugins_uniapp_cli_node_modules_css_loader_dist_cjs_js_ref_8_oneOf_1_1_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_loaders_stylePostLoader_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_8_oneOf_1_2_HBuilderX_plugins_uniapp_cli_node_modules_postcss_loader_src_index_js_ref_8_oneOf_1_3_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_sass_loader_dist_cjs_js_ref_8_oneOf_1_4_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_8_oneOf_1_5_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_detail_vue_vue_type_style_index_0_lang_scss___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/mini-css-extract-plugin/dist/loader.js??ref--8-oneOf-1-0!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/css-loader/dist/cjs.js??ref--8-oneOf-1-1!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/vue-cli-plugin-uni/packages/vue-loader/lib/loaders/stylePostLoader.js!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/vue-cli-plugin-uni/packages/webpack-preprocess-loader??ref--8-oneOf-1-2!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/postcss-loader/src??ref--8-oneOf-1-3!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/vue-cli-plugin-uni/packages/sass-loader/dist/cjs.js??ref--8-oneOf-1-4!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/vue-cli-plugin-uni/packages/webpack-preprocess-loader??ref--8-oneOf-1-5!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/vue-cli-plugin-uni/packages/vue-loader/lib??vue-loader-options!../../../../../HBuilderX/plugins/uniapp-cli/node_modules/@dcloudio/webpack-uni-mp-loader/lib/style.js!./detail.vue?vue&type=style&index=0&lang=scss& */ 63);
/* harmony import */ var _HBuilderX_plugins_uniapp_cli_node_modules_mini_css_extract_plugin_dist_loader_js_ref_8_oneOf_1_0_HBuilderX_plugins_uniapp_cli_node_modules_css_loader_dist_cjs_js_ref_8_oneOf_1_1_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_loaders_stylePostLoader_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_8_oneOf_1_2_HBuilderX_plugins_uniapp_cli_node_modules_postcss_loader_src_index_js_ref_8_oneOf_1_3_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_sass_loader_dist_cjs_js_ref_8_oneOf_1_4_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_8_oneOf_1_5_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_detail_vue_vue_type_style_index_0_lang_scss___WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_HBuilderX_plugins_uniapp_cli_node_modules_mini_css_extract_plugin_dist_loader_js_ref_8_oneOf_1_0_HBuilderX_plugins_uniapp_cli_node_modules_css_loader_dist_cjs_js_ref_8_oneOf_1_1_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_loaders_stylePostLoader_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_8_oneOf_1_2_HBuilderX_plugins_uniapp_cli_node_modules_postcss_loader_src_index_js_ref_8_oneOf_1_3_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_sass_loader_dist_cjs_js_ref_8_oneOf_1_4_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_8_oneOf_1_5_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_detail_vue_vue_type_style_index_0_lang_scss___WEBPACK_IMPORTED_MODULE_0__);
/* harmony reexport (unknown) */ for(var __WEBPACK_IMPORT_KEY__ in _HBuilderX_plugins_uniapp_cli_node_modules_mini_css_extract_plugin_dist_loader_js_ref_8_oneOf_1_0_HBuilderX_plugins_uniapp_cli_node_modules_css_loader_dist_cjs_js_ref_8_oneOf_1_1_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_loaders_stylePostLoader_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_8_oneOf_1_2_HBuilderX_plugins_uniapp_cli_node_modules_postcss_loader_src_index_js_ref_8_oneOf_1_3_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_sass_loader_dist_cjs_js_ref_8_oneOf_1_4_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_8_oneOf_1_5_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_detail_vue_vue_type_style_index_0_lang_scss___WEBPACK_IMPORTED_MODULE_0__) if(["default"].indexOf(__WEBPACK_IMPORT_KEY__) < 0) (function(key) { __webpack_require__.d(__webpack_exports__, key, function() { return _HBuilderX_plugins_uniapp_cli_node_modules_mini_css_extract_plugin_dist_loader_js_ref_8_oneOf_1_0_HBuilderX_plugins_uniapp_cli_node_modules_css_loader_dist_cjs_js_ref_8_oneOf_1_1_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_loaders_stylePostLoader_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_8_oneOf_1_2_HBuilderX_plugins_uniapp_cli_node_modules_postcss_loader_src_index_js_ref_8_oneOf_1_3_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_sass_loader_dist_cjs_js_ref_8_oneOf_1_4_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_8_oneOf_1_5_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_detail_vue_vue_type_style_index_0_lang_scss___WEBPACK_IMPORTED_MODULE_0__[key]; }) }(__WEBPACK_IMPORT_KEY__));
 /* harmony default export */ __webpack_exports__["default"] = (_HBuilderX_plugins_uniapp_cli_node_modules_mini_css_extract_plugin_dist_loader_js_ref_8_oneOf_1_0_HBuilderX_plugins_uniapp_cli_node_modules_css_loader_dist_cjs_js_ref_8_oneOf_1_1_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_loaders_stylePostLoader_js_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_8_oneOf_1_2_HBuilderX_plugins_uniapp_cli_node_modules_postcss_loader_src_index_js_ref_8_oneOf_1_3_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_sass_loader_dist_cjs_js_ref_8_oneOf_1_4_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_webpack_preprocess_loader_index_js_ref_8_oneOf_1_5_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_vue_cli_plugin_uni_packages_vue_loader_lib_index_js_vue_loader_options_HBuilderX_plugins_uniapp_cli_node_modules_dcloudio_webpack_uni_mp_loader_lib_style_js_detail_vue_vue_type_style_index_0_lang_scss___WEBPACK_IMPORTED_MODULE_0___default.a); 

/***/ }),

/***/ 63:
/*!*************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/mini-css-extract-plugin/dist/loader.js??ref--8-oneOf-1-0!./node_modules/css-loader/dist/cjs.js??ref--8-oneOf-1-1!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/webpack-preprocess-loader??ref--8-oneOf-1-2!./node_modules/postcss-loader/src??ref--8-oneOf-1-3!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/sass-loader/dist/cjs.js??ref--8-oneOf-1-4!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/webpack-preprocess-loader??ref--8-oneOf-1-5!./node_modules/@dcloudio/vue-cli-plugin-uni/packages/vue-loader/lib??vue-loader-options!./node_modules/@dcloudio/webpack-uni-mp-loader/lib/style.js!I:/基于在线评论的旅游景点智能推荐系统/小程序/前端/pages/detail/detail.vue?vue&type=style&index=0&lang=scss& ***!
  \*************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

// extracted by mini-css-extract-plugin
    if(false) { var cssReload; }
  

/***/ })

},[[56,"common/runtime","common/vendor"]]]);
//# sourceMappingURL=../../../.sourcemap/mp-weixin/pages/detail/detail.js.map