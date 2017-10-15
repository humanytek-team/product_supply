# -*- coding: utf-8 -*-
###############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2017 Humanytek (<www.humanytek.com>).
#    Rubén Bravo <rubenred18@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from odoo import api, models
import logging
import datetime
_logger = logging.getLogger(__name__)


class ProductSupply(models.TransientModel):
    _name = "product.supply"

    @api.multi
    def confirm(self):
        StockMove = self.env['stock.move']
        stock_moves = StockMove.browse(self._context.get('active_ids'))
        list_prod = []
        list_qty = []
        list_ids = []
        list_brand = []
        list_new_ids = []
        for stock_move in stock_moves:

            reserved_qty = stock_move.reserved_availability
            reserved_qty_lote = 0

            for lote in stock_move.reserved_quant_ids:
                band = False
                qty = lote.qty
                lote_name = lote.lot_id.name
                lote_id = lote.lot_id.id
                reserved_qty_lote += qty
                cont = 0
                for l, lot in list_ids:
                    if stock_move.product_id.id == l and lot == lote_id:
                        list_qty[cont] = list_qty[cont] + qty
                        band = True
                        break
                    cont += 1
                if not band:
                    list_ids.append((stock_move.product_id.id, lote_id))
                    list_prod.append((stock_move.product_id.name, stock_move.product_id.default_code, lote_name))
                    list_brand.append(stock_move.product_id.product_brand_id.name)
                    list_qty.append(qty)
            if reserved_qty_lote < reserved_qty:
                qty = reserved_qty - reserved_qty_lote
                cont = 0
                for l, lot in list_ids:
                    if stock_move.product_id.id == l and lot == -1:
                        list_qty[cont] = list_qty[cont] + qty
                        band = True
                        break
                    cont += 1
                if not band:
                    list_ids.append((stock_move.product_id.id, -1))
                    list_prod.append((stock_move.product_id.name, stock_move.product_id.default_code, ''))
                    list_brand.append(stock_move.product_id.product_brand_id.name)
                    list_qty.append(qty)
        data = dict()
        extra_data = dict()
        #data['ids'] = []
        for l, q in list_ids:
            list_new_ids.append(l)
        data['ids'] = list_new_ids
        extra_data['date'] = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        extra_data['origin'] = stock_moves[0].location_id.name
        extra_data['dest'] = stock_moves[0].location_dest_id.name
        #data['list_prod'] = list_prod
        list_end = []
        cont = 0
        cont_2 = 0
        lista = []
        count = 0
        for l, default_code, lote_name in list_prod:
            if cont_2 == 0:
                brand = list_brand[cont]
                count = list_brand.count(brand)
                lista = []
            t = (l, list_qty[cont], default_code, lote_name)
            cont_2 += 1
            lista.append(t)
            if cont_2 == count:
                tup = (brand, lista)
                list_end.append(tup)
                cont_2 = 0
                count = 0
            cont += 1
        extra_data['list_pro'] = list_end
        data['extra_data'] = extra_data
        Report = self.env['report']
        return Report.get_action(
            self,
            'product_supply.report_supply', data=data)


