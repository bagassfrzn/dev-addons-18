from odoo import http
from odoo.http import request

class BrandImageController(http.Controller):
    @http.route('/about-us', type='http',auth='public',website=True)
    def about_us(self,**kw):
        return request.render('tmi_web.about_us_template')
    
    @http.route('/portofolio', type='http',auth='public',website=True)
    def about_is(self,**kw):
        return request.render('tmi_web.our_portofolio_template')

    @http.route('/products', type='http', auth='public', website=True)
    def our_product(self,**kw):
        our_products = request.env['our.product'].sudo().search(
            [('is_published','=',True)],
            order='sequence asc'
        )
        our_services = request.env['our.service'].sudo().search(
            [('is_published','=',True)],
            order='sequence asc'
        )
        our_clients = request.env['our.client'].sudo().search(
            [('is_published','=',True)],
            order='sequence asc'
        )
        return request.render('tmi_web.our_product_template',{
            'our_products':our_products,
            'our_services':our_services,
            'our_clients':our_clients

        })

    @http.route('/', type='http', auth='public', website=True) # DIUBAH: URL
    def show_brands(self, **kw):
        """
        Controller to fetch and display published brand logos.
        """
        # Cari semua logo brand yang berstatus 'is_published = True'
        brands = request.env['image.brand'].sudo().search( # DIUBAH: Model
            [('is_published', '=', True)],
            order='sequence asc'
        )

        our_clients = request.env['our.client'].sudo().search(
            [('is_published','=',True)],
            order='sequence asc'
        )

        our_services = request.env['our.service'].sudo().search(
            [('is_published','=',True)],
            order='sequence asc',limit=4
        )
        our_areas = request.env['our.area'].sudo().search(
            [('is_published','=',True)],
            order='sequence asc'
        )

        # Render template dan kirim data 'brands' ke template
        return request.render('tmi_web.brand_page_template', { # DIUBAH: ID Template
            'brands': brands, # DIUBAH: Nama variabel
            'our_clients':our_clients,
            'our_services':our_services,
            'our_areas':our_areas
        })