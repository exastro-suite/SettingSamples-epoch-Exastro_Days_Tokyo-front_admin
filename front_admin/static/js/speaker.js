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

  // 登壇者登録ボタン
  const registerModalData = {
    'type': 'input',
    'title': '登壇者登録',
    'contents': [
      {'title': '登壇者名','name': 'speaker_name', 'type': 'text'},
      {'title': 'プロフィール','name': 'speaker_profile', 'type': 'text'},
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
          'speaker_name': "",
          'speaker_profile': "",
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
              url: '/speaker',
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

  // 登壇者詳細表示＆更新ボタン
  const updateModalData = {
    'type': 'input',
    'title': '登壇者更新',
    'contents': [
      {'title': '登壇者名','name': 'speaker_name', 'type': 'text'},
      {'title': 'プロフィール','name': 'speaker_profile', 'type': 'text'},
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
        url: '/speaker/' + event_path,
        async: false
      })
      .done((data, textStatus, jqXHR) => {

        var updateEventData = data;

        const $modal = m.open( updateModalData, updateEventData, {
          'update': function(){
            // 更新処理
            const value = m.getValue();
            console.log(value);

            bodyData = {'speaker_id': event_path};
            $.each(value, function(index, val) {
              $.extend(bodyData, val);
            });

            $.ajax({
              type: 'PUT',
              url: '/speaker/' + event_path,
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
    'title': '登壇者削除',
    'contents': [
      {'title': '登壇者名','name': 'speaker_name', 'type': 'text'},
      {'title': 'プロフィール','name': 'speaker_profile', 'type': 'text'},
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
        url: '/speaker/' + event_path,
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
              url: '/speaker/' + event_path,
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
