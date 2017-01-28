import { KeyboardEvent } from '@angular/platform-browser/src/facade/browser';

import { Inject, Injectable } from '@angular/core';
import { Http, RequestMethod, Response } from '@angular/http';
import { Headers, RequestOptions } from '@angular/http';


import { Observable }     from 'rxjs/Observable';
import { Label } from '../models/label';
import { CardComment } from '../models/comment';
import { DjangoTrelloStatsService } from './djangotrellostats.service';
import { Card } from '../models/card';
import { Board } from '../models/board';
import { List } from '../models/list';


import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';
import 'rxjs/add/operator/toPromise';

//import { Observable }     from 'rxjs/Observable';

@Injectable()
export class CardService extends DjangoTrelloStatsService {

  private ADD_SE_URL = "http://localhost:8000/api/board/{board_id}/card/{card_id}/time";
  private ADD_COMMENT_URL = "http://localhost:8000/api/board/{board_id}/card/{card_id}/comment";
  private COMMENT_URL = "http://localhost:8000/api/board/{board_id}/card/{card_id}/comment/{comment_id}";
  private CHANGE_LIST_URL = "http://localhost:8000/api/board/{board_id}/card/{card_id}/list";
  private CHANGE_LABELS_URL = "http://localhost:8000/api/board/{board_id}/card/{card_id}/labels";

  constructor (http: Http) {
    super(http);
  }

  changeList(card: Card, new_list: List): Promise<Card> {
    let chage_list_url = this.prepareUrl(this.CHANGE_LIST_URL, card);
    return this.http.post(chage_list_url, {new_list: new_list.id})
                  .toPromise()
                  .then(this.extractData)
                  .catch(this.handleError);
  }

  changeCardLabels(card: Card, new_labels_id: number[]): Promise<Card> {
    let chage_labels_url = this.prepareUrl(this.CHANGE_LABELS_URL, card);
    return this.http.post(chage_labels_url, {labels: new_labels_id})
                  .toPromise()
                  .then(this.extractData)
                  .catch(this.handleError);
  }

  addNewComment(card: Card, comment_content: string) : Promise<CardComment> {
    let add_new_comment_url = this.prepareUrl(this.ADD_COMMENT_URL, card);
    return this.http.put(add_new_comment_url, {content: comment_content})
                  .toPromise()
                  .then(this.extractData)
                  .catch(this.handleError);
  }

  editComment(card: Card, comment: CardComment, new_content: string) : Promise<CardComment> {
    let comment_id = comment.id.toString();
    let comment_url = this.prepareUrl(this.COMMENT_URL, card).replace("{comment_id}", comment_id);
    return this.http.post(comment_url, {content: new_content})
                  .toPromise()
                  .then(this.extractData)
                  .catch(this.handleError);
  }

  deleteComment(card: Card, comment: CardComment) : Promise<CardComment> {
    let comment_id = comment.id.toString();
    let comment_url = this.prepareUrl(this.COMMENT_URL, card).replace("{comment_id}", comment_id);
    return this.http.delete(comment_url)
                  .toPromise()
                  .then(this.extractData)
                  .catch(this.handleError);
  }

  addSETime(card: Card, date: string, spent_time:number, estimated_time: number, description: string){
    let add_se_url = this.prepareUrl(this.ADD_SE_URL, card);
    let post_body = {date: date, spent_time: spent_time, estimated_time: estimated_time, description: description};
    return this.http.post(add_se_url, post_body)
                  .toPromise()
                  .then(this.extractData)
                  .catch(this.handleError);
  }

  private prepareUrl(url: string, card: Card): string{
    let board_id = card.board.id.toString();
    let card_id = card.id.toString();
    return url.replace(/\{board_id\}/, board_id).replace(/\{card_id\}/, card_id);
  }

}