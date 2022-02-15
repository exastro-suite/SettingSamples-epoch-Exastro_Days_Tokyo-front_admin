/*
#   Copyright 2022 NEC Corporation
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
*/
// JavaScript Document
;

$(function(){

  const loadClassName = 'loading';
  const m = new modal();

  // Adminメニュー
  const $adminMenu = $('#adminMenu');
  const registerModalData = {
    'type': 'input',
    'title': 'イベント登録',
    'contents': [
      {'title': 'イベント名','name': 'event_name', 'type': 'text'},
      {'title': '開催場所','name': 'event_venue', 'type': 'text'},
      {'title': '開催日','name': 'event_date', 'type': 'date'},
      {'title': 'イベント概要','name': 'event_overview', 'type': 'text'},
    ],
    'commands': [
      {'close': '閉じる'},
      {'register': '登録する'},
    ]
  };

  $adminMenu.find('.adminMenuButton').on('click', function(){
    const $b = $( this ),
          type = $b.attr('data-type');
    switch( type ) {
      case 'register': {

        const newEmptyData = {
          'event_name': "",
          'event_venue': "",
          'event_date': "",
          'event_overview': "",
        };
        const $modal = m.open( registerModalData, newEmptyData, {
          'register': function(){
            // 登録処理
            const value = m.getValue();
            console.log(value);

            bodyData = {};
            $.each(value, function(index, val) {
              $.extend(bodyData, val);
            });
            $.ajax({
              type: 'POST',
              url: '/event',
              contentType: 'application/json',
              data: JSON.stringify(bodyData),
              async: false
            })
            .done((data, textStatus, jqXHR) => {

              window.location.reload();
            })
            .fail((jqXHR, textStatus, errorThrown) => {
              
              alert('登録に失敗しました。');
            });
          }
        } );

      } break;
    }
  });

  // イベント詳細表示＆更新ボタン
  const updateModalData = {
    'type': 'input',
    'title': 'イベント更新',
    'contents': [
      {'title': 'イベント名','name': 'event_name', 'type': 'text'},
      {'title': '開催場所','name': 'event_venue', 'type': 'text'},
      {'title': '開催日','name': 'event_date', 'type': 'date'},
      {'title': 'イベント概要','name': 'event_overview', 'type': 'text'},
    ],
    'commands': [
      {'close': '閉じる'},
      {'update': '更新する'},
    ]
  };

  $('.blockList').find('.event').not('.nodata').on({
    'click': function( event ){
      event.stopPropagation();

      const $event = $( this ),
            event_path = $event.attr('data-event-path');

      if (!event_path) {
        console.error("event_path not set.");
        return;
      }

      $.ajax({
        type: 'GET',
        url: '/event/' + event_path,
        async: false
      })
      .done((data, textStatus, jqXHR) => {

        var updateEventData = data;

        const $modal = m.open( updateModalData, updateEventData, {
          'update': function(){
            // 更新処理
            const value = m.getValue();
            console.log(value);

            bodyData = {'event_id': event_path};
            $.each(value, function(index, val) {
              $.extend(bodyData, val);
            });

            $.ajax({
              type: 'PUT',
              url: '/event/' + event_path,
              contentType: 'application/json',
              data: JSON.stringify(bodyData),
              async: false
            })
            .done((data, textStatus, jqXHR) => {

              window.location.reload();
            })
            .fail((jqXHR, textStatus, errorThrown) => {
              
              alert('更新に失敗しました。');
            });
          }
        } );
      })
      .fail((jqXHR, textStatus, errorThrown) => {
        
        alert('データ読み込みに失敗しました。');
      });
    }
  });

  // 個別削除ボタン
  const deleteModalData = {
    'type': 'view',
    'title': 'イベント削除',
    'contents': [
      {'title': 'イベント名','name': 'event_name', 'type': 'text'},
      {'title': '開催場所','name': 'event_venue', 'type': 'text'},
      {'title': '開催日','name': 'event_date', 'type': 'date'},
      {'title': 'イベント概要','name': 'event_overview', 'type': 'text'},
    ],
    'commands': [
      {'close': '閉じる'},
      {'delete': '削除する'},
    ]
  };

  $('.blockList').find('.eventButton').on({
    'click': function( event ){
      event.stopPropagation();

      const $event = $( this ).closest('.event'),
            event_path = $event.attr('data-event-path');

      $.ajax({
        type: 'GET',
        url: '/event/' + event_path,
        async: false
      })
      .done((data, textStatus, jqXHR) => {

        var deleteEventData = data;

        const $modal = m.open( deleteModalData, deleteEventData, {
          'delete': function(){
            // 削除処理
            const value = m.getValue();
            console.log(value);

            $.ajax({
              type: 'DELETE',
              url: '/event/' + event_path,
              contentType: 'application/json',
              data: JSON.stringify({}),
              async: false
            })
            .done((data, textStatus, jqXHR) => {

              window.location.reload();
            })
            .fail((jqXHR, textStatus, errorThrown) => {
              
              alert('削除に失敗しました。');
            });
          }
        } );
      })
      .fail((jqXHR, textStatus, errorThrown) => {
        
        alert('データ読み込みに失敗しました。');
      });
    }
  });
});
