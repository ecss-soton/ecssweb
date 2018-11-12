from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import CommitteeRoleMember, Society, Sponsor


class CommitteeSitemap(Sitemap):
    changefreq = 'yearly'

    def items(self):
        return CommitteeRoleMember.objects.all()

    def location(self, item):
        return reverse('website:committee-member', kwargs={'role': item.role_codename})


class SocietySitemap(Sitemap):
    def items(self):
        return Society.objects.all()

    def location(self, item):
        return reverse('website:societies', kwargs={'society': item.codename})


class SponsorSitemap(Sitemap):
    def items(self):
        return Sponsor.objects.all()

    def location(self, item):
        return '{}?sponsor={}'.format(reverse('website:sponsors'), item.codename)


class StaticViewSitemap(Sitemap):
    def items(self):
        return [
            'home',
            'committee-overview',
            #'societies-overview',
            'sponsors',
            'events',
            'socials',
            'gaming-socials',
            'welfare',
            'sports',
            'football',
            'netball',
            'running',
            'sports_others',
            'about',
            'contact',
            'media-notice',
            'jumpstart-2018',
        ]

    def location(self, item):
        return reverse('website:{}'.format(item))
