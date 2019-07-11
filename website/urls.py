from django.urls import path, re_path, reverse_lazy
from django.views.generic.base import RedirectView
from django.contrib.sitemaps.views import sitemap

from . import views
from .sitemaps import StaticViewSitemap, CommitteeSitemap, SocietySitemap, SponsorSitemap
from election.views import support_shareable

app_name='website'

sitemaps = {
    'static': StaticViewSitemap,
    'committee': CommitteeSitemap,
    'societies': SocietySitemap,
    'sponsor': SponsorSitemap,
}

urlpatterns = [
    path('', views.home, name='home'),

    re_path(r'^elections/(?P<election>[\w-]+)/support/$', support_shareable, name='election-support-shareable'),

    path('jumpstart/', RedirectView.as_view(pattern_name='website:jumpstart-2019'), name='jumpstart-redirect'),
    path('campus-hack/', RedirectView.as_view(pattern_name='website:campus-hack-19'), name='merch-redirect'),
    path('feedback/', RedirectView.as_view(pattern_name='feedback:submit', permanent=True), name='feedback-redirect'),
    path('shop/', RedirectView.as_view(pattern_name='shop:shop', permanent=True), name='shop-redirect'),
    path('elections/', RedirectView.as_view(pattern_name='election:elections'), name='elections-redirect'),
    path('merch/', RedirectView.as_view(pattern_name='shop:merch1819'), name='merch-redirect'),
    path('agm/', RedirectView.as_view(pattern_name='election:results'), name='voteresults-redirect-2'),
    path('voteresults/', RedirectView.as_view(pattern_name='election:results', permanent=True), name='voteresults-redirect'),


    # Committee
    path('committee/', views.committee_overview, name='committee-overview'),
    re_path(r'^committee/(?P<role>[\w-]+)/$', views.committee_member, name='committee-member'),

    # Societies
    path('societies/', views.societies, name='societies'),
    re_path(r'^societies/(?P<society>[\w-]+)/$', views.societies_detail, name='societies-details'),

    # Sponsors
    path('sponsors/', views.sponsors, name='sponsors'),

    # Events
    path('events/', views.events, name='events'),
    path('events/socials/', views.socials, name='socials'),
    path('events/gaming-socials/', views.gaming_socials, name='gaming-socials'),
    path('events/jumpstart-2018/', RedirectView.as_view(pattern_name='website:jumpstart-2018', permanent=True), name='jumpstart-2018-redirect'),
    path('events/campus-hack-19/', views.campus_hack_19, name='campus-hack-19'),

    # Welfare
    path('welfare/', views.welfare, name='welfare'),

    # Sports
    path('sports/', views.sports, name='sports'),
    path('sports/football/', views.football, name='football'),
    path('sports/netball/', views.netball, name='netball'),
    path('sports/running/', views.running, name='running'),
    path('sports/others/', views.sports_others, name='sports-others'),

    # Freshers
    path('jumpstart-2018/', views.jumpstart_2018, name='jumpstart-2018'),
    path('freshers/jumpstart/', views.jumpstart_2019, name='jumpstart-2019'),


    # About
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # Meta pages
    path('media-notice/', views.media_notice, name='media-notice'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]
