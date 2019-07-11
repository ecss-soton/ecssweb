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
    changefreq = 'yearly'

    def items(self):
        return Society.objects.all()

    def location(self, item):
        return reverse('website:societies-details', kwargs={'society': item.codename})


class SponsorSitemap(Sitemap):
    changefreq = 'monthly'

    def items(self):
        return Sponsor.objects.all()

    def location(self, item):
        return '{}?sponsor={}'.format(reverse('website:sponsors'), item.codename)


class StaticViewSitemap(Sitemap):

    def items(self):
        return [
            'home',
            'committee-overview',
            'societies',
            'sponsors',
            'events',
            'socials',
            'gaming-socials',
            'welfare',
            'sports',
            'football',
            'netball',
            'running',
            'sports-others',
            'about',
            'contact',
            'media-notice',
            'jumpstart-2018',
            'jumpstart-2019',
            'campus-hack-19',
        ]

    def location(self, item):
        return reverse('website:{}'.format(item))
